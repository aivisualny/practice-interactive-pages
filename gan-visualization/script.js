// SVG 설정
const width = 1000;
const height = 600;
const margin = { top: 50, right: 50, bottom: 50, left: 50 };

const svg = d3.select('#visualization')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

// 툴크 생성
const tooltip = d3.select('body')
    .append('div')
    .attr('class', 'tooltip')
    .style('opacity', 0);

// GAN 구조 데이터 정의
const nodes = [
    { id: 'input', name: '랜덤 노이즈', x: 100, y: 300, type: 'input' },
    { id: 'generator', name: '생성자(Generator)', x: 300, y: 300, type: 'network' },
    { id: 'fake', name: '가짜 이미지', x: 500, y: 300, type: 'data' },
    { id: 'discriminator', name: '판별자(Discriminator)', x: 700, y: 300, type: 'network' },
    { id: 'real', name: '실제 이미지', x: 500, y: 150, type: 'data' },
    { id: 'output', name: '판별 결과', x: 900, y: 300, type: 'output' }
];

const links = [
    { source: 'input', target: 'generator' },
    { source: 'generator', target: 'fake' },
    { source: 'fake', target: 'discriminator' },
    { source: 'real', target: 'discriminator' },
    { source: 'discriminator', target: 'output' }
];

// 노드 그리기
const nodeGroup = svg.selectAll('.node')
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('transform', d => `translate(${d.x}, ${d.y})`);

// 노드 원형 그리기
nodeGroup.append('circle')
    .attr('r', 40)
    .style('fill', d => {
        switch(d.type) {
            case 'input': return '#E3F2FD';
            case 'network': return '#C8E6C9';
            case 'data': return '#FFECB3';
            case 'output': return '#FFCDD2';
            default: return '#fff';
        }
    });

// 노드 텍스트 추가
nodeGroup.append('text')
    .text(d => d.name)
    .attr('text-anchor', 'middle')
    .attr('dy', 5)
    .style('font-size', '12px');

// 링크 그리기
const linkGroup = svg.selectAll('.link')
    .data(links)
    .enter()
    .append('path')
    .attr('class', 'link')
    .attr('d', d => {
        const source = nodes.find(n => n.id === d.source);
        const target = nodes.find(n => n.id === d.target);
        return `M${source.x},${source.y} L${target.x},${target.y}`;
    });

// 화살표 추가
svg.append('defs').selectAll('marker')
    .data(['arrow'])
    .enter()
    .append('marker')
    .attr('id', d => d)
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 15)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#999');

// 링크에 화살표 추가
linkGroup.attr('marker-end', 'url(#arrow)');

// 인터랙티브 기능 추가
nodeGroup
    .on('mouseover', function(event, d) {
        tooltip.transition()
            .duration(200)
            .style('opacity', .9);
        tooltip.html(`
            <strong>${d.name}</strong><br/>
            ${getNodeDescription(d)}
        `)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 28) + 'px');
    })
    .on('mouseout', function() {
        tooltip.transition()
            .duration(500)
            .style('opacity', 0);
    });

// 노드 설명 함수
function getNodeDescription(node) {
    const descriptions = {
        'input': '랜덤 노이즈 벡터로, 생성자의 입력값으로 사용됩니다.',
        'generator': '랜덤 노이즈를 입력받아 가짜 이미지를 생성하는 신경망입니다.',
        'fake': '생성자가 만들어낸 가짜 이미지입니다.',
        'discriminator': '실제 이미지와 가짜 이미지를 구분하는 신경망입니다.',
        'real': '학습에 사용되는 실제 이미지 데이터입니다.',
        'output': '판별자가 내놓은 이미지의 진위 여부 판단 결과입니다.'
    };
    return descriptions[node.id] || '';
}

// 설명 텍스트 추가
svg.append('text')
    .attr('x', width / 2)
    .attr('y', margin.top / 2)
    .attr('text-anchor', 'middle')
    .style('font-size', '16px')
    .text('GAN의 기본 구조와 데이터 흐름');

// 내부 구조 데이터 정의
const discriminatorStructure = {
    layers: [
        { id: 'd_input', name: '입력층', x: 700, y: 200, type: 'layer' },
        { id: 'd_conv1', name: '합성곱층 1', x: 700, y: 300, type: 'layer' },
        { id: 'd_conv2', name: '합성곱층 2', x: 700, y: 400, type: 'layer' },
        { id: 'd_output', name: '출력층', x: 700, y: 500, type: 'layer' }
    ],
    connections: [
        { source: 'd_input', target: 'd_conv1' },
        { source: 'd_conv1', target: 'd_conv2' },
        { source: 'd_conv2', target: 'd_output' }
    ]
};

const generatorStructure = {
    layers: [
        { id: 'g_input', name: '입력층', x: 300, y: 200, type: 'layer' },
        { id: 'g_deconv1', name: '역합성곱층 1', x: 300, y: 300, type: 'layer' },
        { id: 'g_deconv2', name: '역합성곱층 2', x: 300, y: 400, type: 'layer' },
        { id: 'g_output', name: '출력층', x: 300, y: 500, type: 'layer' }
    ],
    connections: [
        { source: 'g_input', target: 'g_deconv1' },
        { source: 'g_deconv1', target: 'g_deconv2' },
        { source: 'g_deconv2', target: 'g_output' }
    ]
};

// 내부 구조를 그리는 함수
function drawInternalStructure(structure, parentId) {
    const parentNode = nodes.find(n => n.id === parentId);
    if (!parentNode) return;

    // 내부 구조 컨테이너 생성
    const container = svg.append('g')
        .attr('class', `internal-structure ${parentId}-structure`)
        .style('opacity', 0);

    // 레이어 그리기
    const layerGroup = container.selectAll('.layer')
        .data(structure.layers)
        .enter()
        .append('g')
        .attr('class', 'layer')
        .attr('transform', d => `translate(${d.x}, ${d.y})`);

    // 레이어 원형 그리기
    layerGroup.append('circle')
        .attr('r', 30)
        .style('fill', '#E8F5E9')
        .style('stroke', '#4CAF50')
        .style('stroke-width', 2);

    // 레이어 텍스트 추가
    layerGroup.append('text')
        .text(d => d.name)
        .attr('text-anchor', 'middle')
        .attr('dy', 5)
        .style('font-size', '10px');

    // 연결선 그리기
    const linkGroup = container.selectAll('.internal-link')
        .data(structure.connections)
        .enter()
        .append('path')
        .attr('class', 'internal-link')
        .attr('d', d => {
            const source = structure.layers.find(l => l.id === d.source);
            const target = structure.layers.find(l => l.id === d.target);
            return `M${source.x},${source.y} L${target.x},${target.y}`;
        })
        .style('stroke', '#4CAF50')
        .style('stroke-width', 1.5)
        .style('fill', 'none');

    // 데이터 흐름 애니메이션
    const flowAnimation = () => {
        linkGroup.each(function() {
            const path = d3.select(this);
            const length = path.node().getTotalLength();
            
            path.attr('stroke-dasharray', length)
                .attr('stroke-dashoffset', length)
                .transition()
                .duration(2000)
                .ease(d3.easeLinear)
                .attr('stroke-dashoffset', 0)
                .on('end', function() {
                    d3.select(this)
                        .attr('stroke-dashoffset', length)
                        .transition()
                        .duration(2000)
                        .ease(d3.easeLinear)
                        .attr('stroke-dashoffset', 0);
                });
        });
    };

    // 애니메이션 시작
    flowAnimation();
}

// 노드 클릭 이벤트 수정
nodeGroup
    .on('click', function(event, d) {
        if (d.id === 'discriminator') {
            // 기존 내부 구조 제거
            svg.selectAll('.discriminator-structure').remove();
            // 판별자 내부 구조 표시
            drawInternalStructure(discriminatorStructure, 'discriminator');
            svg.select('.discriminator-structure')
                .transition()
                .duration(500)
                .style('opacity', 1);
        } else if (d.id === 'generator') {
            // 기존 내부 구조 제거
            svg.selectAll('.generator-structure').remove();
            // 생성자 내부 구조 표시
            drawInternalStructure(generatorStructure, 'generator');
            svg.select('.generator-structure')
                .transition()
                .duration(500)
                .style('opacity', 1);
        } else {
            // 다른 노드 클릭 시 내부 구조 숨기기
            svg.selectAll('.internal-structure')
                .transition()
                .duration(500)
                .style('opacity', 0)
                .remove();
        }
    }); 