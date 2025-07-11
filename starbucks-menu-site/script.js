// 스크롤 시 헤더에 그림자 효과 추가
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 10) {
        header.style.boxShadow = '0 4px 16px rgba(0,0,0,0.08)';
    } else {
        header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    }
});

// 메뉴 클릭 시 부드럽게 이동 (HTML에 scroll-behavior: smooth 적용되어 있음)
// 추가 인터랙션이 필요하다면 여기에 작성하세요. 