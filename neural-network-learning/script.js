document.addEventListener('DOMContentLoaded', () => {
    // 각 단계에 애니메이션 효과 추가
    const steps = document.querySelectorAll('.step');
    steps.forEach(step => {
        step.addEventListener('mouseenter', () => {
            step.style.transform = 'translateY(-10px)';
        });

        step.addEventListener('mouseleave', () => {
            step.style.transform = 'translateY(0)';
        });
    });

    // 순전파 애니메이션
    const forwardProp = document.querySelector('.forward-prop');
    if (forwardProp) {
        const neurons = forwardProp.querySelectorAll('.neuron');
        let currentIndex = 0;

        function animateForwardProp() {
            neurons.forEach(n => n.style.backgroundColor = '#3498db');
            
            if (currentIndex < neurons.length) {
                neurons[currentIndex].style.backgroundColor = '#e74c3c';
                currentIndex = (currentIndex + 1) % neurons.length;
            }
        }

        forwardProp.addEventListener('mouseenter', () => {
            currentIndex = 0;
            const interval = setInterval(animateForwardProp, 800);
            forwardProp.dataset.interval = interval;
        });

        forwardProp.addEventListener('mouseleave', () => {
            clearInterval(forwardProp.dataset.interval);
            neurons.forEach(n => n.style.backgroundColor = '#3498db');
        });
    }

    // 역전파 애니메이션
    const backProp = document.querySelector('.back-prop');
    if (backProp) {
        const neurons = backProp.querySelectorAll('.neuron');
        let currentIndex = neurons.length - 1;

        function animateBackProp() {
            neurons.forEach(n => n.style.backgroundColor = '#3498db');
            
            if (currentIndex >= 0) {
                neurons[currentIndex].style.backgroundColor = '#e74c3c';
                currentIndex = (currentIndex - 1 + neurons.length) % neurons.length;
            }
        }

        backProp.addEventListener('mouseenter', () => {
            currentIndex = neurons.length - 1;
            const interval = setInterval(animateBackProp, 800);
            backProp.dataset.interval = interval;
        });

        backProp.addEventListener('mouseleave', () => {
            clearInterval(backProp.dataset.interval);
            neurons.forEach(n => n.style.backgroundColor = '#3498db');
        });
    }

    // 벡터화 시각화에 하이라이트 효과
    const vectorization = document.querySelector('.vectorization');
    if (vectorization) {
        vectorization.addEventListener('mouseenter', () => {
            const matrices = vectorization.querySelectorAll('.matrix pre');
            matrices.forEach(matrix => {
                matrix.style.backgroundColor = '#e8f4f8';
            });
        });

        vectorization.addEventListener('mouseleave', () => {
            const matrices = vectorization.querySelectorAll('.matrix pre');
            matrices.forEach(matrix => {
                matrix.style.backgroundColor = '#f8f9fa';
            });
        });
    }

    // 코드 예제에 구문 강조 효과
    const codeExample = document.querySelector('.implementation-example pre');
    if (codeExample) {
        const code = codeExample.textContent;
        const keywords = ['class', 'def', 'self', 'return', 'import'];
        let highlightedCode = code;
        
        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            highlightedCode = highlightedCode.replace(
                regex,
                `<span style="color: #e74c3c;">${keyword}</span>`
            );
        });

        codeExample.innerHTML = `<code>${highlightedCode}</code>`;
    }
}); 