// 기술 데이터
const techData = {
    imagen: {
        name: 'Imagen Video',
        color: '#ff6b6b',
        metrics: {
            quality: 95,
            speed: 60,
            accessibility: 30
        }
    },
    pvdm: {
        name: 'PVDM',
        color: '#4ecdc4',
        metrics: {
            quality: 80,
            speed: 85,
            accessibility: 70
        }
    },
    videocrafter: {
        name: 'VideoCrafter',
        color: '#45b7d1',
        metrics: {
            quality: 75,
            speed: 70,
            accessibility: 90
        }
    }
};

// DOM 요소들
const compareBtn = document.getElementById('compare-btn');
const animateBtn = document.getElementById('animate-btn');
const resetBtn = document.getElementById('reset-btn');
const chartCanvas = document.getElementById('comparison-chart');
const techCards = document.querySelectorAll('.tech-card');

// Canvas 설정
const ctx = chartCanvas.getContext('2d');
let animationId = null;

// 차트 그리기 함수
function drawChart(data = null) {
    const width = chartCanvas.width;
    const height = chartCanvas.height;
    
    // 캔버스 초기화
    ctx.clearRect(0, 0, width, height);
    
    if (!data) {
        // 기본 차트 그리기
        drawDefaultChart();
        return;
    }
    
    // 데이터 기반 차트 그리기
    drawDataChart(data);
}

// 기본 차트 그리기
function drawDefaultChart() {
    const width = chartCanvas.width;
    const height = chartCanvas.height;
    
    // 배경
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, width, height);
    
    // 제목
    ctx.fillStyle = '#2c3e50';
    ctx.font = 'bold 24px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('AI 비디오 생성 기술 비교', width / 2, 40);
    
    // 설명
    ctx.font = '16px Arial';
    ctx.fillStyle = '#7f8c8d';
    ctx.fillText('버튼을 클릭하여 인터랙티브 차트를 확인하세요', width / 2, 70);
    
    // 데모 그래프
    drawDemoGraph();
}

// 데모 그래프 그리기
function drawDemoGraph() {
    const width = chartCanvas.width;
    const height = chartCanvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    
    // 원형 그래프
    const radius = 80;
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1'];
    const labels = ['품질', '속도', '접근성'];
    
    let currentAngle = -Math.PI / 2;
    const sliceAngle = (2 * Math.PI) / 3;
    
    for (let i = 0; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = colors[i];
        ctx.fill();
        
        // 라벨
        const labelAngle = currentAngle + sliceAngle / 2;
        const labelX = centerX + Math.cos(labelAngle) * (radius + 30);
        const labelY = centerY + Math.sin(labelAngle) * (radius + 30);
        
        ctx.fillStyle = '#2c3e50';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(labels[i], labelX, labelY);
        
        currentAngle += sliceAngle;
    }
}

// 데이터 기반 차트 그리기
function drawDataChart(data) {
    const width = chartCanvas.width;
    const height = chartCanvas.height;
    
    // 배경
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, width, height);
    
    // 제목
    ctx.fillStyle = '#2c3e50';
    ctx.font = 'bold 24px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('성능 비교 차트', width / 2, 40);
    
    // 막대 그래프 그리기
    drawBarChart(data);
    
    // 레이더 차트 그리기
    drawRadarChart(data);
}

// 막대 그래프 그리기
function drawBarChart(data) {
    const width = chartCanvas.width;
    const height = chartCanvas.height;
    const chartWidth = width * 0.8;
    const chartHeight = height * 0.3;
    const startX = (width - chartWidth) / 2;
    const startY = 80;
    
    const technologies = Object.keys(data);
    const metrics = ['quality', 'speed', 'accessibility'];
    const metricLabels = ['품질', '속도', '접근성'];
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1'];
    
    const barWidth = chartWidth / (technologies.length * metrics.length + 1);
    const maxValue = 100;
    
    // Y축
    ctx.strokeStyle = '#bdc3c7';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = startY + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(startX, y);
        ctx.lineTo(startX + chartWidth, y);
        ctx.stroke();
        
        // Y축 라벨
        ctx.fillStyle = '#7f8c8d';
        ctx.font = '12px Arial';
        ctx.textAlign = 'right';
        ctx.fillText(`${(maxValue / 5) * (5 - i)}`, startX - 10, y + 4);
    }
    
    // 막대 그리기
    technologies.forEach((tech, techIndex) => {
        metrics.forEach((metric, metricIndex) => {
            const value = data[tech].metrics[metric];
            const barHeight = (value / maxValue) * chartHeight;
            const x = startX + (techIndex * metrics.length + metricIndex + 1) * barWidth;
            const y = startY + chartHeight - barHeight;
            
            // 막대
            ctx.fillStyle = colors[metricIndex];
            ctx.fillRect(x, y, barWidth * 0.8, barHeight);
            
            // 값 표시
            ctx.fillStyle = '#2c3e50';
            ctx.font = 'bold 12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`${value}%`, x + barWidth * 0.4, y - 5);
        });
    });
    
    // X축 라벨
    ctx.fillStyle = '#2c3e50';
    ctx.font = 'bold 14px Arial';
    ctx.textAlign = 'center';
    technologies.forEach((tech, index) => {
        const x = startX + (index * metrics.length + 1.5) * barWidth;
        ctx.fillText(data[tech].name, x, startY + chartHeight + 25);
    });
}

// 레이더 차트 그리기
function drawRadarChart(data) {
    const width = chartCanvas.width;
    const height = chartCanvas.height;
    const centerX = width / 2;
    const centerY = height * 0.75;
    const radius = 100;
    
    const technologies = Object.keys(data);
    const metrics = ['quality', 'speed', 'accessibility'];
    const metricLabels = ['품질', '속도', '접근성'];
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1'];
    
    // 레이더 차트 그리드
    ctx.strokeStyle = '#ecf0f1';
    ctx.lineWidth = 1;
    for (let i = 1; i <= 5; i++) {
        const currentRadius = (radius / 5) * i;
        ctx.beginPath();
        for (let j = 0; j < metrics.length; j++) {
            const angle = (2 * Math.PI * j) / metrics.length - Math.PI / 2;
            const x = centerX + Math.cos(angle) * currentRadius;
            const y = centerY + Math.sin(angle) * currentRadius;
            if (j === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.closePath();
        ctx.stroke();
    }
    
    // 축 그리기
    ctx.strokeStyle = '#bdc3c7';
    ctx.lineWidth = 2;
    metrics.forEach((metric, index) => {
        const angle = (2 * Math.PI * index) / metrics.length - Math.PI / 2;
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.stroke();
        
        // 축 라벨
        ctx.fillStyle = '#2c3e50';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        const labelX = centerX + Math.cos(angle) * (radius + 20);
        const labelY = centerY + Math.sin(angle) * (radius + 20);
        ctx.fillText(metricLabels[index], labelX, labelY);
    });
    
    // 데이터 포인트 그리기
    technologies.forEach((tech, techIndex) => {
        const techColor = colors[techIndex];
        
        ctx.beginPath();
        metrics.forEach((metric, metricIndex) => {
            const value = data[tech].metrics[metric];
            const angle = (2 * Math.PI * metricIndex) / metrics.length - Math.PI / 2;
            const pointRadius = (value / 100) * radius;
            const x = centerX + Math.cos(angle) * pointRadius;
            const y = centerY + Math.sin(angle) * pointRadius;
            
            if (metricIndex === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        ctx.closePath();
        
        // 영역 채우기
        ctx.fillStyle = techColor + '20';
        ctx.fill();
        
        // 테두리
        ctx.strokeStyle = techColor;
        ctx.lineWidth = 3;
        ctx.stroke();
        
        // 포인트
        metrics.forEach((metric, metricIndex) => {
            const value = data[tech].metrics[metric];
            const angle = (2 * Math.PI * metricIndex) / metrics.length - Math.PI / 2;
            const pointRadius = (value / 100) * radius;
            const x = centerX + Math.cos(angle) * pointRadius;
            const y = centerY + Math.sin(angle) * pointRadius;
            
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, 2 * Math.PI);
            ctx.fillStyle = techColor;
            ctx.fill();
        });
    });
    
    // 범례
    drawLegend(data, colors);
}

// 범례 그리기
function drawLegend(data, colors) {
    const width = chartCanvas.width;
    const height = chartCanvas.height;
    const startX = 50;
    const startY = height - 80;
    
    Object.keys(data).forEach((tech, index) => {
        const x = startX + index * 200;
        const y = startY;
        
        // 색상 박스
        ctx.fillStyle = colors[index];
        ctx.fillRect(x, y, 20, 20);
        
        // 라벨
        ctx.fillStyle = '#2c3e50';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(data[tech].name, x + 30, y + 15);
    });
}

// 애니메이션 함수
function animateChart() {
    let progress = 0;
    const duration = 2000; // 2초
    const startTime = Date.now();
    
    function animate() {
        const currentTime = Date.now();
        progress = Math.min((currentTime - startTime) / duration, 1);
        
        // 보간된 데이터 생성
        const interpolatedData = {};
        Object.keys(techData).forEach(tech => {
            interpolatedData[tech] = {
                name: techData[tech].name,
                color: techData[tech].color,
                metrics: {}
            };
            
            Object.keys(techData[tech].metrics).forEach(metric => {
                interpolatedData[tech].metrics[metric] = Math.round(techData[tech].metrics[metric] * progress);
            });
        });
        
        drawDataChart(interpolatedData);
        
        if (progress < 1) {
            animationId = requestAnimationFrame(animate);
        }
    }
    
    animate();
}

// 카드 애니메이션
function animateCards() {
    techCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('animate');
            setTimeout(() => {
                card.classList.remove('animate');
            }, 2000);
        }, index * 300);
    });
}

// 이벤트 리스너
compareBtn.addEventListener('click', () => {
    drawDataChart(techData);
});

animateBtn.addEventListener('click', () => {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    animateChart();
    animateCards();
});

resetBtn.addEventListener('click', () => {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    drawChart();
});

// 카드 호버 효과
techCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-15px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
    });
});

// 프로그레스 바 애니메이션
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, Math.random() * 1000);
    });
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    drawChart();
    animateProgressBars();
    
    // 스크롤 애니메이션
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.tech-card, .comparison-table, .interactive-demo').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// 반응형 차트 크기 조정
window.addEventListener('resize', () => {
    const container = chartCanvas.parentElement;
    const containerWidth = container.clientWidth - 40; // 패딩 고려
    
    chartCanvas.width = Math.min(800, containerWidth);
    chartCanvas.height = 400;
    
    drawChart();
}); 