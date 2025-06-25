document.addEventListener('DOMContentLoaded', () => {
    const contentImageUpload = document.getElementById('content-image-upload');
    const contentImagePreview = document.getElementById('content-image-preview');
    const styleImages = document.querySelectorAll('.style-image');
    const styleImagePreview = document.getElementById('style-image-preview');
    const transferButton = document.getElementById('transfer-button');
    const resultImage = document.getElementById('result-image');
    const resultPlaceholder = document.querySelector('.result-area .placeholder');
    const loader = document.getElementById('loader');

    let contentFile = null;
    let selectedStyleImage = null;
    let model = null;

    // AI 모델 초기화 함수 (TensorFlow.js 직접 사용)
    async function initializeModel() {
        try {
            transferButton.disabled = true;
            resultPlaceholder.textContent = 'AI 모델을 로딩 중입니다...';
            loader.style.display = 'block';

            // TF Hub에서 직접 모델을 로드합니다.
            const modelUrl = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/tfjs/2';
            model = await tf.loadGraphModel(modelUrl);

            loader.style.display = 'none';
            resultPlaceholder.textContent = '결과가 여기에 표시됩니다.';
            updateButtonState();
        } catch (error) {
            console.error('모델 초기화 실패:', error);
            resultPlaceholder.textContent = 'AI 모델 로딩에 실패했습니다. 네트워크 연결을 확인하고 페이지를 새로고침 해주세요.';
        }
    }

    // 버튼 상태 업데이트 함수
    function updateButtonState() {
        transferButton.disabled = !(contentFile && selectedStyleImage && model);
    }

    contentImageUpload.addEventListener('change', (event) => {
        if (event.target.files && event.target.files[0]) {
            contentFile = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                contentImagePreview.src = e.target.result;
                contentImagePreview.style.display = 'block';
            };
            reader.readAsDataURL(contentFile);
            updateButtonState();
        }
    });

    styleImages.forEach(img => {
        img.addEventListener('click', () => {
            styleImages.forEach(i => i.classList.remove('selected'));
            img.classList.add('selected');
            selectedStyleImage = img;
            styleImagePreview.src = img.src;
            styleImagePreview.style.display = 'block';
            updateButtonState();
        });
    });

    // '스타일 변환 시작' 버튼 클릭 처리 (실제 AI 모델 사용)
    transferButton.addEventListener('click', async () => {
        if (!contentFile || !selectedStyleImage || !model) return;

        loader.style.display = 'block';
        resultPlaceholder.style.display = 'none';
        resultImage.style.display = 'none';
        transferButton.disabled = true;

        try {
            await tf.nextFrame(); // UI 업데이트를 위한 시간 확보
            
            const contentImg = document.getElementById('content-image-preview');
            const styleImg = selectedStyleImage;

            // tf.tidy를 사용하여 텐서 메모리를 자동으로 관리합니다.
            const stylizedResult = tf.tidy(() => {
                // 이미지를 텐서로 변환하고 정규화합니다.
                const contentTensor = tf.browser.fromPixels(contentImg).toFloat().div(tf.scalar(255)).expandDims();
                const styleTensor = tf.browser.fromPixels(styleImg).toFloat().div(tf.scalar(255)).expandDims();
                
                // AI 모델을 실행합니다.
                return model.execute([contentTensor, styleTensor]);
            });

            const canvas = document.createElement('canvas');
            canvas.width = contentImg.width;
            canvas.height = contentImg.height;
            await tf.browser.toPixels(stylizedResult.squeeze(), canvas);
            
            resultImage.src = canvas.toDataURL('image/jpeg');
            resultImage.style.display = 'block';

        } catch (error) {
            console.error("스타일 변환 중 오류:", error);
            resultPlaceholder.textContent = '오류가 발생했습니다. 이미지 크기가 너무 크거나 메모리가 부족할 수 있습니다.';
            resultPlaceholder.style.display = 'block';
        } finally {
            loader.style.display = 'none';
            updateButtonState();
        }
    });

    initializeModel();
}); 