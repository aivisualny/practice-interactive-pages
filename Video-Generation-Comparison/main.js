console.log("비디오 생성 모델 분석 페이지 스크립트가 로드되었습니다.");

// 향후 인터랙티브 기능을 여기에 추가할 수 있습니다.
// 예: 모델 카드 필터링, 정렬, 차트 렌더링 등 

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function() {
    // 스크롤 애니메이션
    initScrollAnimations();
    
    // 모델 카드 인터랙션
    initModelCardInteractions();
    
    // 성능 비교 차트 (간단한 시각화)
    initPerformanceVisualization();
    
    // 부드러운 스크롤
    initSmoothScroll();
    
    // 모델 비교 기능
    initModelComparison();
});

// 스크롤 애니메이션 초기화
function initScrollAnimations() {
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

    // 애니메이션 대상 요소들
    const animatedElements = document.querySelectorAll('.performance-card, .model-card, .trend-card, .comparison-split');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// 모델 카드 인터랙션
function initModelCardInteractions() {
    const modelCards = document.querySelectorAll('.model-card');
    
    modelCards.forEach(card => {
        // 카드 클릭 시 상세 정보 토글
        const header = card.querySelector('.model-header');
        if (header) {
            header.addEventListener('click', function() {
                const content = card.querySelector('.model-content');
                if (content) {
                    content.style.display = content.style.display === 'none' ? 'grid' : 'none';
                    card.classList.toggle('collapsed');
                }
            });
            
            // 커서 스타일 변경
            header.style.cursor = 'pointer';
        }
        
        // 태그 클릭 이벤트
        const tags = card.querySelectorAll('.tag');
        tags.forEach(tag => {
            tag.addEventListener('click', function(e) {
                e.stopPropagation();
                highlightSimilarModels(tag.textContent);
            });
        });
    });
}

// 유사한 모델 하이라이트
function highlightSimilarModels(tagText) {
    const allCards = document.querySelectorAll('.model-card');
    const similarTags = document.querySelectorAll(`.tag:contains('${tagText}')`);
    
    // 모든 카드에서 하이라이트 제거
    allCards.forEach(card => {
        card.style.opacity = '0.5';
        card.style.transform = 'scale(0.95)';
    });
    
    // 유사한 태그를 가진 카드들 하이라이트
    similarTags.forEach(tag => {
        const card = tag.closest('.model-card');
        if (card) {
            card.style.opacity = '1';
            card.style.transform = 'scale(1.02)';
            card.style.boxShadow = '0 12px 30px rgba(0,123,255,0.3)';
        }
    });
    
    // 3초 후 원래 상태로 복원
    setTimeout(() => {
        allCards.forEach(card => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
            card.style.boxShadow = '';
        });
    }, 3000);
}

// 성능 시각화 초기화
function initPerformanceVisualization() {
    const performanceCards = document.querySelectorAll('.performance-card');
    
    performanceCards.forEach(card => {
        const metrics = card.querySelectorAll('.metric');
        
        metrics.forEach(metric => {
            const score = metric.querySelector('.score');
            const rank = metric.querySelector('.rank');
            
            if (score && rank) {
                // FVD 점수에 따른 색상 변경
                const scoreText = score.textContent;
                if (scoreText.includes('FVD:')) {
                    const fvdValue = parseFloat(scoreText.match(/[\d.]+/)[0]);
                    if (fvdValue < 10) {
                        rank.style.color = '#28a745'; // 녹색 (우수)
                    } else if (fvdValue < 50) {
                        rank.style.color = '#ffc107'; // 노란색 (보통)
                    } else if (fvdValue < 100) {
                        rank.style.color = '#fd7e14'; // 주황색 (보통)
                    } else {
                        rank.style.color = '#dc3545'; // 빨간색 (낮음)
                    }
                }
                
                // 선호도에 따른 색상 변경
                if (scoreText.includes('선호도')) {
                    const preferenceValue = parseFloat(scoreText.match(/[\d.]+/)[0]);
                    if (preferenceValue > 70) {
                        rank.style.color = '#28a745'; // 녹색 (우수)
                    } else if (preferenceValue > 40) {
                        rank.style.color = '#ffc107'; // 노란색 (보통)
                    } else {
                        rank.style.color = '#dc3545'; // 빨간색 (낮음)
                    }
                }
                
                // 순위에 따른 애니메이션
                if (rank.textContent.includes('🥇')) {
                    rank.style.animation = 'goldPulse 2s infinite';
                } else if (rank.textContent.includes('🥈')) {
                    rank.style.animation = 'silverPulse 2s infinite';
                } else if (rank.textContent.includes('🥉')) {
                    rank.style.animation = 'bronzePulse 2s infinite';
                }
            }
        });
    });
}

// 모델 비교 기능 초기화
function initModelComparison() {
    const comparisonTable = document.querySelector('.comparison-table table');
    if (comparisonTable) {
        const rows = comparisonTable.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            row.addEventListener('click', function() {
                // 행 클릭 시 해당 특성 하이라이트
                const cells = this.querySelectorAll('td');
                const feature = cells[0].textContent;
                
                // 모든 행에서 하이라이트 제거
                rows.forEach(r => r.style.backgroundColor = '');
                
                // 클릭된 행 하이라이트
                this.style.backgroundColor = '#e3f2fd';
                
                // 2초 후 원래 상태로 복원
                setTimeout(() => {
                    this.style.backgroundColor = '';
                }, 2000);
            });
        });
    }
}

// 부드러운 스크롤 초기화
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// CSS 애니메이션 추가
const style = document.createElement('style');
style.textContent = `
    @keyframes goldPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes silverPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes bronzePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    
    .model-card.collapsed .model-content {
        display: none;
    }
    
    .model-card.collapsed {
        max-height: 200px;
        overflow: hidden;
    }
    
    .performance-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric:hover {
        background-color: #f8f9fa;
        border-radius: 4px;
        padding: 0.8rem;
        margin: 0 -0.8rem;
    }
    
    .tag:hover {
        transform: scale(1.05);
        cursor: pointer;
    }
    
    .comparison-table tbody tr:hover td {
        background-color: #e3f2fd;
        transition: background-color 0.3s ease;
    }
    
    .comparison-table tbody tr {
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    
    .comparison-left:hover,
    .comparison-right:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .trend-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
`;
document.head.appendChild(style);

// 성능 데이터 시각화 (간단한 차트)
function createPerformanceChart() {
    const chartContainer = document.createElement('div');
    chartContainer.className = 'performance-chart';
    chartContainer.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 2rem 0;
    `;
    
    chartContainer.innerHTML = `
        <h3>성능 비교 차트</h3>
        <div style="display: flex; justify-content: space-around; align-items: end; height: 200px; margin-top: 2rem;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="background: #28a745; width: 60px; height: 80px; border-radius: 4px 4px 0 0;"></div>
                <span style="margin-top: 0.5rem; font-weight: 600;">W.A.LT-XL</span>
                <span style="font-size: 0.8rem; color: #666;">FVD: 36</span>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="background: #ffc107; width: 60px; height: 60px; border-radius: 4px 4px 0 0;"></div>
                <span style="margin-top: 0.5rem; font-weight: 600;">W.A.LT-L</span>
                <span style="font-size: 0.8rem; color: #666;">FVD: 46</span>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="background: #fd7e14; width: 60px; height: 50px; border-radius: 4px 4px 0 0;"></div>
                <span style="margin-top: 0.5rem; font-weight: 600;">MAGVIT</span>
                <span style="font-size: 0.8rem; color: #666;">FVD: 58</span>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="background: #dc3545; width: 60px; height: 30px; border-radius: 4px 4px 0 0;"></div>
                <span style="margin-top: 0.5rem; font-weight: 600;">StyleSV</span>
                <span style="font-size: 0.8rem; color: #666;">FVD: 221</span>
            </div>
        </div>
    `;
    
    // 성능 비교 섹션에 차트 추가
    const performanceSection = document.getElementById('performance-comparison');
    if (performanceSection) {
        performanceSection.appendChild(chartContainer);
    }
}

// 페이지 로드 완료 후 차트 생성
window.addEventListener('load', function() {
    setTimeout(createPerformanceChart, 1000);
}); 