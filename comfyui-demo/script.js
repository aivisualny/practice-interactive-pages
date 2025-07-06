// ComfyUI 데모 JavaScript
class ComfyUIDemo {
    constructor() {
        this.nodes = new Map();
        this.connections = [];
        this.selectedNode = null;
        this.draggedNode = null;
        this.connectionStart = null;
        this.nodeCounter = 0;
        this.isDragging = false;
        this.dragOffset = { x: 0, y: 0 };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
        this.updateStatus();
    }

    setupEventListeners() {
        // 버튼 이벤트
        document.getElementById('runWorkflow').addEventListener('click', () => this.runWorkflow());
        document.getElementById('clearCanvas').addEventListener('click', () => this.clearCanvas());
        document.getElementById('close-modal').addEventListener('click', () => this.closeModal());

        // 캔버스 이벤트
        const canvas = document.getElementById('canvas');
        canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));

        // 키보드 이벤트
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));

        // 모달 외부 클릭 시 닫기
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('node-modal');
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }

    setupDragAndDrop() {
        const nodeItems = document.querySelectorAll('.node-item');
        const canvas = document.getElementById('canvas');

        nodeItems.forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', item.dataset.nodeType);
                e.dataTransfer.effectAllowed = 'copy';
            });
        });

        canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        });

        canvas.addEventListener('drop', (e) => {
            e.preventDefault();
            const nodeType = e.dataTransfer.getData('text/plain');
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.createNode(nodeType, x, y);
        });
    }

    createNode(type, x, y) {
        const nodeId = `node_${++this.nodeCounter}`;
        const node = {
            id: nodeId,
            type: type,
            x: x,
            y: y,
            data: this.getDefaultNodeData(type)
        };

        this.nodes.set(nodeId, node);
        this.renderNode(node);
        this.updateStatus();
        this.hideDropHint();
    }

    getDefaultNodeData(type) {
        const defaults = {
            'prompt': {
                text: 'a beautiful landscape, high quality, detailed',
                label: '프롬프트'
            },
            'negative-prompt': {
                text: 'blurry, low quality, distorted',
                label: '네거티브 프롬프트'
            },
            'seed': {
                value: Math.floor(Math.random() * 1000000),
                label: '시드'
            },
            'checkpoint': {
                model: 'stable-diffusion-v1-5',
                label: '체크포인트'
            },
            'lora': {
                model: 'none',
                strength: 0.8,
                label: 'LoRA'
            },
            'ksampler': {
                steps: 20,
                cfg: 7.0,
                sampler: 'euler',
                scheduler: 'normal',
                label: 'K-Sampler'
            },
            'vae': {
                model: 'auto',
                label: 'VAE'
            },
            'save-image': {
                filename: 'generated_image',
                label: '이미지 저장'
            },
            'preview': {
                label: '미리보기'
            }
        };

        return defaults[type] || { label: type };
    }

    renderNode(node) {
        const canvas = document.getElementById('canvas');
        const nodeElement = document.createElement('div');
        nodeElement.className = 'canvas-node';
        nodeElement.id = node.id;
        nodeElement.style.left = `${node.x}px`;
        nodeElement.style.top = `${node.y}px`;

        const iconMap = {
            'prompt': 'fas fa-keyboard',
            'negative-prompt': 'fas fa-ban',
            'seed': 'fas fa-dice',
            'checkpoint': 'fas fa-cube',
            'lora': 'fas fa-layer-group',
            'ksampler': 'fas fa-cogs',
            'vae': 'fas fa-compress',
            'save-image': 'fas fa-save',
            'preview': 'fas fa-eye'
        };

        const icon = iconMap[node.type] || 'fas fa-puzzle-piece';

        nodeElement.innerHTML = `
            <div class="node-header">
                <span><i class="${icon}"></i>${node.data.label}</span>
                <button class="node-close" onclick="comfyUI.removeNode('${node.id}')">&times;</button>
            </div>
            <div class="node-content">
                ${this.generateNodeContent(node)}
            </div>
        `;

        // 노드 이벤트 리스너
        nodeElement.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectNode(node.id);
        });

        nodeElement.addEventListener('dblclick', (e) => {
            e.stopPropagation();
            this.openNodeModal(node.id);
        });

        canvas.appendChild(nodeElement);
    }

    generateNodeContent(node) {
        const content = [];
        
        // 입력 소켓들
        if (['ksampler', 'vae', 'save-image', 'preview'].includes(node.type)) {
            content.push('<div class="node-input"><span class="input-label">모델</span><div class="input-socket" data-socket="model"></div></div>');
        }
        
        if (['ksampler'].includes(node.type)) {
            content.push('<div class="node-input"><span class="input-label">프롬프트</span><div class="input-socket" data-socket="prompt"></div></div>');
            content.push('<div class="node-input"><span class="input-label">네거티브</span><div class="input-socket" data-socket="negative"></div></div>');
        }

        // 출력 소켓들
        if (['prompt', 'negative-prompt', 'seed', 'checkpoint', 'lora'].includes(node.type)) {
            content.push('<div class="node-output"><span class="output-label">출력</span><div class="output-socket" data-socket="output"></div></div>');
        }
        
        if (['ksampler', 'vae'].includes(node.type)) {
            content.push('<div class="node-output"><span class="output-label">이미지</span><div class="output-socket" data-socket="image"></div></div>');
        }

        return content.join('');
    }

    selectNode(nodeId) {
        // 이전 선택 해제
        if (this.selectedNode) {
            const prevNode = document.getElementById(this.selectedNode);
            if (prevNode) prevNode.classList.remove('selected');
        }

        // 새 노드 선택
        this.selectedNode = nodeId;
        const nodeElement = document.getElementById(nodeId);
        if (nodeElement) {
            nodeElement.classList.add('selected');
        }

        this.updateNodeProperties();
    }

    updateNodeProperties() {
        const propertiesPanel = document.getElementById('node-properties');
        
        if (!this.selectedNode) {
            propertiesPanel.innerHTML = '<p class="no-selection">노드를 선택하여 속성을 편집하세요</p>';
            return;
        }

        const node = this.nodes.get(this.selectedNode);
        if (!node) return;

        let html = `<h4>${node.data.label}</h4>`;
        
        switch (node.type) {
            case 'prompt':
            case 'negative-prompt':
                html += `
                    <div class="form-group">
                        <label>텍스트</label>
                        <textarea id="node-text" rows="3">${node.data.text}</textarea>
                    </div>
                `;
                break;
            case 'seed':
                html += `
                    <div class="form-group">
                        <label>시드 값</label>
                        <input type="number" id="node-seed" value="${node.data.value}">
                    </div>
                `;
                break;
            case 'checkpoint':
                html += `
                    <div class="form-group">
                        <label>모델</label>
                        <select id="node-model">
                            <option value="stable-diffusion-v1-5" ${node.data.model === 'stable-diffusion-v1-5' ? 'selected' : ''}>Stable Diffusion v1.5</option>
                            <option value="stable-diffusion-v2-1" ${node.data.model === 'stable-diffusion-v2-1' ? 'selected' : ''}>Stable Diffusion v2.1</option>
                            <option value="stable-diffusion-xl" ${node.data.model === 'stable-diffusion-xl' ? 'selected' : ''}>Stable Diffusion XL</option>
                        </select>
                    </div>
                `;
                break;
            case 'ksampler':
                html += `
                    <div class="form-group">
                        <label>스텝 수</label>
                        <input type="number" id="node-steps" min="1" max="100" value="${node.data.steps}">
                    </div>
                    <div class="form-group">
                        <label>CFG 스케일</label>
                        <input type="number" id="node-cfg" min="1" max="20" step="0.1" value="${node.data.cfg}">
                    </div>
                    <div class="form-group">
                        <label>샘플러</label>
                        <select id="node-sampler">
                            <option value="euler" ${node.data.sampler === 'euler' ? 'selected' : ''}>Euler</option>
                            <option value="euler_a" ${node.data.sampler === 'euler_a' ? 'selected' : ''}>Euler Ancestral</option>
                            <option value="dpm++" ${node.data.sampler === 'dpm++' ? 'selected' : ''}>DPM++ 2M</option>
                        </select>
                    </div>
                `;
                break;
        }

        html += `<button class="btn btn-primary" onclick="comfyUI.saveNodeProperties()">저장</button>`;
        propertiesPanel.innerHTML = html;
    }

    saveNodeProperties() {
        if (!this.selectedNode) return;

        const node = this.nodes.get(this.selectedNode);
        if (!node) return;

        switch (node.type) {
            case 'prompt':
            case 'negative-prompt':
                node.data.text = document.getElementById('node-text').value;
                break;
            case 'seed':
                node.data.value = parseInt(document.getElementById('node-seed').value);
                break;
            case 'checkpoint':
                node.data.model = document.getElementById('node-model').value;
                break;
            case 'ksampler':
                node.data.steps = parseInt(document.getElementById('node-steps').value);
                node.data.cfg = parseFloat(document.getElementById('node-cfg').value);
                node.data.sampler = document.getElementById('node-sampler').value;
                break;
        }

        this.updateStatus();
    }

    removeNode(nodeId) {
        // 연결 제거
        this.connections = this.connections.filter(conn => 
            conn.from !== nodeId && conn.to !== nodeId
        );

        // 노드 제거
        this.nodes.delete(nodeId);
        const nodeElement = document.getElementById(nodeId);
        if (nodeElement) {
            nodeElement.remove();
        }

        if (this.selectedNode === nodeId) {
            this.selectedNode = null;
            this.updateNodeProperties();
        }

        this.updateStatus();
        this.renderConnections();
    }

    handleCanvasClick(e) {
        if (e.target.id === 'canvas') {
            this.selectNode(null);
        }
    }

    handleMouseDown(e) {
        const nodeElement = e.target.closest('.canvas-node');
        if (nodeElement) {
            this.isDragging = true;
            this.draggedNode = nodeElement.id;
            const rect = nodeElement.getBoundingClientRect();
            this.dragOffset.x = e.clientX - rect.left;
            this.dragOffset.y = e.clientY - rect.top;
            nodeElement.style.cursor = 'grabbing';
        }
    }

    handleMouseMove(e) {
        if (this.isDragging && this.draggedNode) {
            const nodeElement = document.getElementById(this.draggedNode);
            const canvas = document.getElementById('canvas');
            const rect = canvas.getBoundingClientRect();
            
            const x = e.clientX - rect.left - this.dragOffset.x;
            const y = e.clientY - rect.top - this.dragOffset.y;
            
            nodeElement.style.left = `${x}px`;
            nodeElement.style.top = `${y}px`;
            
            const node = this.nodes.get(this.draggedNode);
            if (node) {
                node.x = x;
                node.y = y;
            }
        }
    }

    handleMouseUp(e) {
        if (this.isDragging && this.draggedNode) {
            const nodeElement = document.getElementById(this.draggedNode);
            if (nodeElement) {
                nodeElement.style.cursor = 'move';
            }
        }
        this.isDragging = false;
        this.draggedNode = null;
    }

    handleKeyDown(e) {
        if (e.key === 'Delete' && this.selectedNode) {
            this.removeNode(this.selectedNode);
        }
    }

    openNodeModal(nodeId) {
        const node = this.nodes.get(nodeId);
        if (!node) return;

        const modal = document.getElementById('node-modal');
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');

        modalTitle.textContent = `${node.data.label} 설정`;
        
        let formHtml = '';
        switch (node.type) {
            case 'prompt':
            case 'negative-prompt':
                formHtml = `
                    <div class="form-group">
                        <label>텍스트</label>
                        <textarea id="modal-text" rows="5">${node.data.text}</textarea>
                    </div>
                `;
                break;
            case 'ksampler':
                formHtml = `
                    <div class="form-group">
                        <label>스텝 수</label>
                        <input type="number" id="modal-steps" min="1" max="100" value="${node.data.steps}">
                    </div>
                    <div class="form-group">
                        <label>CFG 스케일</label>
                        <input type="number" id="modal-cfg" min="1" max="20" step="0.1" value="${node.data.cfg}">
                    </div>
                    <div class="form-group">
                        <label>샘플러</label>
                        <select id="modal-sampler">
                            <option value="euler" ${node.data.sampler === 'euler' ? 'selected' : ''}>Euler</option>
                            <option value="euler_a" ${node.data.sampler === 'euler_a' ? 'selected' : ''}>Euler Ancestral</option>
                            <option value="dpm++" ${node.data.sampler === 'dpm++' ? 'selected' : ''}>DPM++ 2M</option>
                        </select>
                    </div>
                `;
                break;
        }

        formHtml += `
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button class="btn btn-primary" onclick="comfyUI.saveModalChanges('${nodeId}')">저장</button>
                <button class="btn btn-secondary" onclick="comfyUI.closeModal()">취소</button>
            </div>
        `;

        modalBody.innerHTML = formHtml;
        modal.style.display = 'block';
    }

    saveModalChanges(nodeId) {
        const node = this.nodes.get(nodeId);
        if (!node) return;

        switch (node.type) {
            case 'prompt':
            case 'negative-prompt':
                node.data.text = document.getElementById('modal-text').value;
                break;
            case 'ksampler':
                node.data.steps = parseInt(document.getElementById('modal-steps').value);
                node.data.cfg = parseFloat(document.getElementById('modal-cfg').value);
                node.data.sampler = document.getElementById('modal-sampler').value;
                break;
        }

        this.closeModal();
        this.updateNodeProperties();
    }

    closeModal() {
        document.getElementById('node-modal').style.display = 'none';
    }

    hideDropHint() {
        const overlay = document.querySelector('.canvas-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    runWorkflow() {
        if (this.nodes.size === 0) {
            this.showStatus('워크플로우에 노드가 없습니다.', 'warning');
            return;
        }

        this.showStatus('워크플로우 실행 중...', 'info');
        
        // 시뮬레이션된 워크플로우 실행
        setTimeout(() => {
            this.generateDemoResult();
            this.showStatus('워크플로우 완료!', 'success');
        }, 2000);
    }

    generateDemoResult() {
        const resultArea = document.getElementById('result-area');
        
        // 데모 이미지 생성 (실제로는 AI 모델이 생성)
        const demoImages = [
            'https://via.placeholder.com/512x512/4CAF50/ffffff?text=AI+Generated+Image+1',
            'https://via.placeholder.com/512x512/2196F3/ffffff?text=AI+Generated+Image+2',
            'https://via.placeholder.com/512x512/FF9800/ffffff?text=AI+Generated+Image+3'
        ];

        const randomImage = demoImages[Math.floor(Math.random() * demoImages.length)];
        
        resultArea.innerHTML = `
            <div style="text-align: center;">
                <h4 style="color: #4CAF50; margin-bottom: 16px;">생성된 이미지</h4>
                <img src="${randomImage}" alt="Generated Image" style="max-width: 100%; border-radius: 8px; margin-bottom: 16px;">
                <div style="font-size: 0.9rem; color: #aaa;">
                    <p>생성 시간: ${new Date().toLocaleTimeString()}</p>
                    <p>노드 수: ${this.nodes.size}</p>
                    <p>연결 수: ${this.connections.length}</p>
                </div>
            </div>
        `;
    }

    clearCanvas() {
        if (confirm('모든 노드와 연결을 삭제하시겠습니까?')) {
            this.nodes.clear();
            this.connections = [];
            this.selectedNode = null;
            
            const canvas = document.getElementById('canvas');
            const nodes = canvas.querySelectorAll('.canvas-node');
            nodes.forEach(node => node.remove());
            
            this.updateStatus();
            this.showDropHint();
        }
    }

    showDropHint() {
        const overlay = document.querySelector('.canvas-overlay');
        if (overlay) {
            overlay.style.display = 'flex';
        }
    }

    updateStatus() {
        document.getElementById('node-count').textContent = `노드: ${this.nodes.size}`;
        document.getElementById('connection-count').textContent = `연결: ${this.connections.length}`;
    }

    showStatus(message, type = 'info') {
        const statusText = document.getElementById('status-text');
        statusText.textContent = message;
        
        // 상태 타입에 따른 색상 변경
        statusText.className = `status-${type}`;
        
        setTimeout(() => {
            statusText.textContent = '준비됨';
            statusText.className = '';
        }, 3000);
    }

    renderConnections() {
        // 연결선 렌더링 로직 (향후 구현)
    }
}

// 전역 인스턴스 생성
const comfyUI = new ComfyUIDemo();

// 전역 함수들
window.removeNode = (nodeId) => comfyUI.removeNode(nodeId);
window.saveNodeProperties = () => comfyUI.saveNodeProperties();
window.saveModalChanges = (nodeId) => comfyUI.saveModalChanges(nodeId);
window.closeModal = () => comfyUI.closeModal(); 