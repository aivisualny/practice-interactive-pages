// 탭 네비게이션
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            
            // 모든 탭 비활성화
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // 선택된 탭 활성화
            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // 각 GAN 기술별 시각화 초기화
    initializeMoCoGAN();
    initializeTGAN();
    initializeStyleGAN();
    initializeComparison();
});

// MoCoGAN 시각화
function initializeMoCoGAN() {
    const canvas = document.getElementById('mocogan-canvas');
    const detailCanvas = document.getElementById('mocogan-detail-canvas');
    const compCanvas = document.getElementById('comp-mocogan');
    
    if (canvas) createMoCoGANVisualization(canvas, 'overview');
    if (detailCanvas) createMoCoGANVisualization(detailCanvas, 'detail');
    if (compCanvas) createMoCoGANVisualization(compCanvas, 'comparison');
}

function createMoCoGANVisualization(canvas, type) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width || 300;
    const height = canvas.height || 200;
    
    canvas.width = width;
    canvas.height = height;
    
    let frame = 0;
    let contentVector = { x: 50, y: 100, size: 20 };
    let motionVector = { x: 0, y: 0 };
    
    function animate() {
        ctx.clearRect(0, 0, width, height);
        
        // 배경 그라데이션
        const gradient = ctx.createLinearGradient(0, 0, width, height);
        gradient.addColorStop(0, '#e3f2fd');
        gradient.addColorStop(1, '#bbdefb');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
        
        // Content Vector (고정된 객체)
        ctx.fillStyle = '#2196f3';
        ctx.beginPath();
        ctx.arc(contentVector.x, contentVector.y, contentVector.size, 0, Math.PI * 2);
        ctx.fill();
        
        // Motion Vector (움직이는 요소)
        const motionX = 150 + Math.sin(frame * 0.05) * 30;
        const motionY = 100 + Math.cos(frame * 0.03) * 20;
        
        ctx.fillStyle = '#ff5722';
        ctx.beginPath();
        ctx.arc(motionX, motionY, 15, 0, Math.PI * 2);
        ctx.fill();
        
        // 연결선
        ctx.strokeStyle = '#666';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(contentVector.x, contentVector.y);
        ctx.lineTo(motionX, motionY);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // 텍스트
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.fillText('Content', contentVector.x - 20, contentVector.y - 30);
        ctx.fillText('Motion', motionX - 15, motionY - 25);
        
        frame++;
        requestAnimationFrame(animate);
    }
    
    animate();
}

// TGAN 시각화
function initializeTGAN() {
    const canvas = document.getElementById('tgan-canvas');
    const detailCanvas = document.getElementById('tgan-detail-canvas');
    const compCanvas = document.getElementById('comp-tgan');
    
    if (canvas) createTGANVisualization(canvas, 'overview');
    if (detailCanvas) createTGANVisualization(detailCanvas, 'detail');
    if (compCanvas) createTGANVisualization(compCanvas, 'comparison');
}

function createTGANVisualization(canvas, type) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width || 300;
    const height = canvas.height || 200;
    
    canvas.width = width;
    canvas.height = height;
    
    let frame = 0;
    let frames = [];
    
    // 프레임 배열 초기화
    for (let i = 0; i < 5; i++) {
        frames.push({
            x: 50 + i * 50,
            y: 100,
            size: 15 + Math.random() * 10,
            color: `hsl(${200 + i * 20}, 70%, 60%)`
        });
    }
    
    function animate() {
        ctx.clearRect(0, 0, width, height);
        
        // 배경
        const gradient = ctx.createLinearGradient(0, 0, width, height);
        gradient.addColorStop(0, '#f3e5f5');
        gradient.addColorStop(1, '#e1bee7');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
        
        // 프레임들 그리기
        frames.forEach((f, index) => {
            ctx.fillStyle = f.color;
            ctx.beginPath();
            ctx.arc(f.x, f.y + Math.sin(frame * 0.05 + index) * 10, f.size, 0, Math.PI * 2);
            ctx.fill();
            
            // 프레임 번호
            ctx.fillStyle = '#333';
            ctx.font = '10px Arial';
            ctx.fillText(`F${index + 1}`, f.x - 5, f.y + 30);
        });
        
        // 시간축
        ctx.strokeStyle = '#666';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(30, 150);
        ctx.lineTo(width - 30, 150);
        ctx.stroke();
        
        // 시간 화살표
        ctx.fillStyle = '#666';
        ctx.beginPath();
        ctx.moveTo(width - 40, 145);
        ctx.lineTo(width - 30, 150);
        ctx.lineTo(width - 40, 155);
        ctx.fill();
        
        ctx.fillText('Time', width - 50, 170);
        
        frame++;
        requestAnimationFrame(animate);
    }
    
    animate();
}

// StyleGAN-V 시각화
function initializeStyleGAN() {
    const canvas = document.getElementById('stylegan-canvas');
    const detailCanvas = document.getElementById('stylegan-detail-canvas');
    const compCanvas = document.getElementById('comp-stylegan');
    
    if (canvas) createStyleGANVisualization(canvas, 'overview');
    if (detailCanvas) createStyleGANVisualization(detailCanvas, 'detail');
    if (compCanvas) createStyleGANVisualization(compCanvas, 'comparison');
}

function createStyleGANVisualization(canvas, type) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width || 300;
    const height = canvas.height || 200;
    
    canvas.width = width;
    canvas.height = height;
    
    let frame = 0;
    let styleVector = { x: 50, y: 50 };
    let noiseVector = { x: 50, y: 150 };
    let output = { x: 200, y: 100 };
    
    function animate() {
        ctx.clearRect(0, 0, width, height);
        
        // 배경
        const gradient = ctx.createLinearGradient(0, 0, width, height);
        gradient.addColorStop(0, '#fff3e0');
        gradient.addColorStop(1, '#ffe0b2');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
        
        // Style Vector
        ctx.fillStyle = '#ff9800';
        ctx.beginPath();
        ctx.arc(styleVector.x, styleVector.y, 20, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.fillText('Style', styleVector.x - 15, styleVector.y - 30);
        
        // Noise Vector
        ctx.fillStyle = '#795548';
        ctx.beginPath();
        ctx.arc(noiseVector.x, noiseVector.y, 15, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#333';
        ctx.fillText('Noise', noiseVector.x - 15, noiseVector.y - 25);
        
        // Output (고품질 비디오)
        const outputSize = 25 + Math.sin(frame * 0.03) * 5;
        ctx.fillStyle = '#4caf50';
        ctx.beginPath();
        ctx.arc(output.x, output.y, outputSize, 0, Math.PI * 2);
        ctx.fill();
        
        // 고품질 효과 (광택)
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.beginPath();
        ctx.arc(output.x - 5, output.y - 5, outputSize * 0.3, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.fillText('High Quality', output.x - 25, output.y + 40);
        
        // 연결선
        ctx.strokeStyle = '#666';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(styleVector.x + 20, styleVector.y);
        ctx.lineTo(output.x - outputSize, output.y);
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(noiseVector.x + 15, noiseVector.y);
        ctx.lineTo(output.x - outputSize, output.y);
        ctx.stroke();
        
        frame++;
        requestAnimationFrame(animate);
    }
    
    animate();
}

// 비교 시각화
function initializeComparison() {
    const compMoCoGAN = document.getElementById('comp-mocogan');
    const compTGAN = document.getElementById('comp-tgan');
    const compStyleGAN = document.getElementById('comp-stylegan');
    
    if (compMoCoGAN) createComparisonMoCoGAN(compMoCoGAN);
    if (compTGAN) createComparisonTGAN(compTGAN);
    if (compStyleGAN) createComparisonStyleGAN(compStyleGAN);
    
    // 비교 컨트롤
    const startAllBtn = document.getElementById('start-all');
    const stopAllBtn = document.getElementById('stop-all');
    const resetAllBtn = document.getElementById('reset-all');
    
    if (startAllBtn) startAllBtn.addEventListener('click', startAllAnimations);
    if (stopAllBtn) stopAllBtn.addEventListener('click', stopAllAnimations);
    if (resetAllBtn) resetAllBtn.addEventListener('click', resetAllAnimations);
}

function createComparisonMoCoGAN(canvas) {
    const ctx = canvas.getContext('2d');
    canvas.width = 250;
    canvas.height = 200;
    
    let frame = 0;
    let isPlaying = true;
    
    function animate() {
        if (!isPlaying) return;
        
        ctx.clearRect(0, 0, 250, 200);
        
        // MoCoGAN 특성: 움직임과 내용 분리
        const contentX = 125;
        const contentY = 100;
        const motionX = 125 + Math.sin(frame * 0.1) * 40;
        const motionY = 100 + Math.cos(frame * 0.08) * 30;
        
        // Content (고정)
        ctx.fillStyle = '#2196f3';
        ctx.beginPath();
        ctx.arc(contentX, contentY, 20, 0, Math.PI * 2);
        ctx.fill();
        
        // Motion (움직임)
        ctx.fillStyle = '#ff5722';
        ctx.beginPath();
        ctx.arc(motionX, motionY, 15, 0, Math.PI * 2);
        ctx.fill();
        
        frame++;
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // 컨트롤 함수들
    window.mocoganControls = {
        play: () => { isPlaying = true; animate(); },
        pause: () => { isPlaying = false; },
        reset: () => { frame = 0; }
    };
}

function createComparisonTGAN(canvas) {
    const ctx = canvas.getContext('2d');
    canvas.width = 250;
    canvas.height = 200;
    
    let frame = 0;
    let isPlaying = true;
    
    function animate() {
        if (!isPlaying) return;
        
        ctx.clearRect(0, 0, 250, 200);
        
        // TGAN 특성: 순차적 프레임 생성
        for (let i = 0; i < 4; i++) {
            const x = 50 + i * 40;
            const y = 100 + Math.sin(frame * 0.05 + i) * 15;
            const size = 12 + Math.sin(frame * 0.03 + i) * 3;
            
            ctx.fillStyle = `hsl(${200 + i * 30}, 70%, 60%)`;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        }
        
        frame++;
        requestAnimationFrame(animate);
    }
    
    animate();
    
    window.tganControls = {
        play: () => { isPlaying = true; animate(); },
        pause: () => { isPlaying = false; },
        reset: () => { frame = 0; }
    };
}

function createComparisonStyleGAN(canvas) {
    const ctx = canvas.getContext('2d');
    canvas.width = 250;
    canvas.height = 200;
    
    let frame = 0;
    let isPlaying = true;
    
    function animate() {
        if (!isPlaying) return;
        
        ctx.clearRect(0, 0, 250, 200);
        
        // StyleGAN-V 특성: 고품질, 스타일 기반
        const centerX = 125;
        const centerY = 100;
        const size = 30 + Math.sin(frame * 0.02) * 5;
        
        // 메인 객체
        ctx.fillStyle = '#4caf50';
        ctx.beginPath();
        ctx.arc(centerX, centerY, size, 0, Math.PI * 2);
        ctx.fill();
        
        // 고품질 효과
        ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.beginPath();
        ctx.arc(centerX - 8, centerY - 8, size * 0.3, 0, Math.PI * 2);
        ctx.fill();
        
        // 스타일 요소들
        for (let i = 0; i < 3; i++) {
            const angle = (frame * 0.05 + i * Math.PI * 2 / 3) % (Math.PI * 2);
            const x = centerX + Math.cos(angle) * 50;
            const y = centerY + Math.sin(angle) * 50;
            
            ctx.fillStyle = `hsl(${300 + i * 60}, 70%, 60%)`;
            ctx.beginPath();
            ctx.arc(x, y, 8, 0, Math.PI * 2);
            ctx.fill();
        }
        
        frame++;
        requestAnimationFrame(animate);
    }
    
    animate();
    
    window.styleganControls = {
        play: () => { isPlaying = true; animate(); },
        pause: () => { isPlaying = false; },
        reset: () => { frame = 0; }
    };
}

function startAllAnimations() {
    if (window.mocoganControls) window.mocoganControls.play();
    if (window.tganControls) window.tganControls.play();
    if (window.styleganControls) window.styleganControls.play();
}

function stopAllAnimations() {
    if (window.mocoganControls) window.mocoganControls.pause();
    if (window.tganControls) window.tganControls.pause();
    if (window.styleganControls) window.styleganControls.pause();
}

function resetAllAnimations() {
    if (window.mocoganControls) window.mocoganControls.reset();
    if (window.tganControls) window.tganControls.reset();
    if (window.styleganControls) window.styleganControls.reset();
}

// 개별 컨트롤 이벤트 리스너
document.addEventListener('DOMContentLoaded', function() {
    // MoCoGAN 컨트롤
    const mocoganPlay = document.getElementById('mocogan-play');
    const mocoganPause = document.getElementById('mocogan-pause');
    const mocoganSpeed = document.getElementById('mocogan-speed');
    
    if (mocoganPlay) mocoganPlay.addEventListener('click', () => {
        if (window.mocoganControls) window.mocoganControls.play();
    });
    
    if (mocoganPause) mocoganPause.addEventListener('click', () => {
        if (window.mocoganControls) window.mocoganControls.pause();
    });
    
    // TGAN 컨트롤
    const tganPlay = document.getElementById('tgan-play');
    const tganPause = document.getElementById('tgan-pause');
    const tganSpeed = document.getElementById('tgan-speed');
    
    if (tganPlay) tganPlay.addEventListener('click', () => {
        if (window.tganControls) window.tganControls.play();
    });
    
    if (tganPause) tganPause.addEventListener('click', () => {
        if (window.tganControls) window.tganControls.pause();
    });
    
    // StyleGAN 컨트롤
    const styleganPlay = document.getElementById('stylegan-play');
    const styleganPause = document.getElementById('stylegan-pause');
    const styleganSpeed = document.getElementById('stylegan-speed');
    
    if (styleganPlay) styleganPlay.addEventListener('click', () => {
        if (window.styleganControls) window.styleganControls.play();
    });
    
    if (styleganPause) styleganPause.addEventListener('click', () => {
        if (window.styleganControls) window.styleganControls.pause();
    });
}); 