document.addEventListener('DOMContentLoaded', () => {
    // 뉴런 생성 함수
    function createNeurons(container, count) {
        for (let i = 0; i < count; i++) {
            const neuron = document.createElement('div');
            neuron.className = 'neuron';
            container.appendChild(neuron);
        }
    }

    // 각 층의 뉴런 컨테이너 선택
    const inputLayerNeurons = document.querySelector('.input-layer .neurons');
    const hiddenLayerNeurons = document.querySelector('.hidden-layer .neurons');
    const outputLayerNeurons = document.querySelector('.output-layer .neurons');

    // 각 층에 뉴런 생성
    createNeurons(inputLayerNeurons, 5);  // 입력층 뉴런 5개
    createNeurons(hiddenLayerNeurons, 3); // 은닉층 뉴런 3개
    createNeurons(outputLayerNeurons, 1); // 출력층 뉴런 1개

    // 뉴런에 호버 이벤트 추가
    const neurons = document.querySelectorAll('.neuron');
    neurons.forEach(neuron => {
        neuron.addEventListener('mouseover', () => {
            neuron.style.backgroundColor = '#e74c3c';
        });

        neuron.addEventListener('mouseout', () => {
            neuron.style.backgroundColor = '#3498db';
        });
    });

    // 층 설명 애니메이션
    const layers = document.querySelectorAll('.layer');
    layers.forEach(layer => {
        layer.addEventListener('click', () => {
            layer.style.transform = 'scale(1.05)';
            setTimeout(() => {
                layer.style.transform = 'translateY(-5px)';
            }, 200);
        });
    });

    // 특징 설명 텍스트에 호버 효과 추가
    const featureTexts = document.querySelectorAll('.feature-explanations p');
    featureTexts.forEach((text, index) => {
        text.addEventListener('mouseover', () => {
            const correspondingNeuron = hiddenLayerNeurons.children[index];
            if (correspondingNeuron) {
                correspondingNeuron.style.backgroundColor = '#e74c3c';
                correspondingNeuron.style.transform = 'scale(1.2)';
            }
        });

        text.addEventListener('mouseout', () => {
            const correspondingNeuron = hiddenLayerNeurons.children[index];
            if (correspondingNeuron) {
                correspondingNeuron.style.backgroundColor = '#3498db';
                correspondingNeuron.style.transform = 'scale(1)';
            }
        });
    });
}); 