// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    // 카드 애니메이션 효과
    animateCards();
    
    // 링크 클릭 이벤트 처리
    setupLinkHandlers();
    
    // 스크롤 효과
    setupScrollEffects();
    
    // 검색 기능 (향후 확장용)
    setupSearchFunctionality();
});

// 카드 애니메이션
function animateCards() {
    const cards = document.querySelectorAll('.project-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// 링크 핸들러 설정
function setupLinkHandlers() {
    const links = document.querySelectorAll('.card-link');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // 링크 클릭 시 시각적 피드백
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // 외부 링크인 경우 새 탭에서 열기
            if (this.getAttribute('href').startsWith('http')) {
                e.preventDefault();
                window.open(this.getAttribute('href'), '_blank');
            }
        });
        
        // 링크 호버 효과
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// 스크롤 효과
function setupScrollEffects() {
    let ticking = false;
    
    function updateScrollEffects() {
        const scrolled = window.pageYOffset;
        const header = document.querySelector('.header');
        
        if (scrolled > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        }
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScrollEffects);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

// 검색 기능 (향후 확장용)
function setupSearchFunctionality() {
    // 검색 입력창이 추가될 경우를 위한 준비
    const searchInput = document.querySelector('#search-input');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const cards = document.querySelectorAll('.project-card');
            
            cards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const description = card.querySelector('.card-description').textContent.toLowerCase();
                const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase());
                
                const matches = title.includes(searchTerm) || 
                              description.includes(searchTerm) || 
                              tags.some(tag => tag.includes(searchTerm));
                
                if (matches || searchTerm === '') {
                    card.style.display = 'block';
                    card.style.opacity = '1';
                } else {
                    card.style.display = 'none';
                    card.style.opacity = '0';
                }
            });
        });
    }
}

// 카테고리 필터링 (향후 확장용)
function filterByCategory(category) {
    const cards = document.querySelectorAll('.project-card');
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    // 버튼 상태 업데이트
    filterButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === category) {
            btn.classList.add('active');
        }
    });
    
    // 카드 필터링
    cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        } else {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.display = 'none';
            }, 300);
        }
    });
}

// 로딩 상태 관리
function showLoading() {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        card.classList.add('loading');
    });
}

function hideLoading() {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        card.classList.remove('loading');
    });
}

// 카드 클릭 통계 (선택사항)
function trackCardClick(projectName) {
    // Google Analytics나 다른 분석 도구와 연동 가능
    console.log(`Project clicked: ${projectName}`);
    
    // 로컬 스토리지에 클릭 기록 저장
    const clicks = JSON.parse(localStorage.getItem('projectClicks') || '{}');
    clicks[projectName] = (clicks[projectName] || 0) + 1;
    localStorage.setItem('projectClicks', JSON.stringify(clicks));
}

// 다크 모드 토글 (향후 확장용)
function toggleDarkMode() {
    const body = document.body;
    const isDark = body.classList.contains('dark-mode');
    
    if (isDark) {
        body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'false');
    } else {
        body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'true');
    }
}

// 페이지 로드 시 다크 모드 상태 복원
function restoreDarkMode() {
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'true') {
        document.body.classList.add('dark-mode');
    }
}

// 초기화
restoreDarkMode();

// 전역 함수로 노출 (필요시)
window.filterByCategory = filterByCategory;
window.toggleDarkMode = toggleDarkMode;
window.trackCardClick = trackCardClick; 