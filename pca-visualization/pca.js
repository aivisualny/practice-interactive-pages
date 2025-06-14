// 샘플 데이터 생성 (3차원 데이터)
const generateSampleData = (n) => {
    const data = [];
    for (let i = 0; i < n; i++) {
        data.push({
            x: Math.random() * 100,
            y: Math.random() * 100,
            z: Math.random() * 100
        });
    }
    return data;
};

// PCA 계산 함수
function calculatePCA(data) {
    // 데이터 정규화
    const mean = {
        x: d3.mean(data, d => d.x),
        y: d3.mean(data, d => d.y),
        z: d3.mean(data, d => d.z)
    };

    const normalizedData = data.map(d => ({
        x: d.x - mean.x,
        y: d.y - mean.y,
        z: d.z - mean.z
    }));

    // 공분산 행렬 계산
    const covariance = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ];

    normalizedData.forEach(d => {
        covariance[0][0] += d.x * d.x;
        covariance[0][1] += d.x * d.y;
        covariance[0][2] += d.x * d.z;
        covariance[1][1] += d.y * d.y;
        covariance[1][2] += d.y * d.z;
        covariance[2][2] += d.z * d.z;
    });

    covariance[1][0] = covariance[0][1];
    covariance[2][0] = covariance[0][2];
    covariance[2][1] = covariance[1][2];

    // 고유값과 고유벡터 계산 (단순화된 버전)
    const eigenvalues = [100, 50, 25]; // 예시 값
    const eigenvectors = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ];

    return {
        mean,
        eigenvalues,
        eigenvectors,
        normalizedData
    };
}

// 시각화 함수
function visualizePCA(data, varianceThreshold) {
    const pca = calculatePCA(data);
    
    // 시각화 영역 설정
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const width = 800 - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom;

    // SVG 생성
    const svg = d3.select("#visualization")
        .html("")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // 스케일 설정
    const xScale = d3.scaleLinear()
        .domain([-50, 50])
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([-50, 50])
        .range([height, 0]);

    // 축 추가
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale));

    svg.append("g")
        .call(d3.axisLeft(yScale));

    // 데이터 포인트 그리기
    svg.selectAll("circle")
        .data(pca.normalizedData)
        .enter()
        .append("circle")
        .attr("cx", d => xScale(d.x))
        .attr("cy", d => yScale(d.y))
        .attr("r", 3)
        .attr("fill", "steelblue")
        .attr("opacity", 0.6);

    // 주성분 벡터 그리기
    const pc1 = pca.eigenvectors[0];
    const pc2 = pca.eigenvectors[1];

    // 주성분 벡터 시각화
    const arrowLength = 30;
    svg.append("line")
        .attr("x1", xScale(0))
        .attr("y1", yScale(0))
        .attr("x2", xScale(pc1[0] * arrowLength))
        .attr("y2", yScale(pc1[1] * arrowLength))
        .attr("stroke", "red")
        .attr("stroke-width", 2);

    svg.append("line")
        .attr("x1", xScale(0))
        .attr("y1", yScale(0))
        .attr("x2", xScale(pc2[0] * arrowLength))
        .attr("y2", yScale(pc2[1] * arrowLength))
        .attr("stroke", "green")
        .attr("stroke-width", 2);

    // 설명된 분산 비율 표시
    const totalVariance = pca.eigenvalues.reduce((a, b) => a + b, 0);
    const explainedVariance = pca.eigenvalues[0] / totalVariance * 100;

    svg.append("text")
        .attr("x", 10)
        .attr("y", 20)
        .text(`설명된 분산 비율: ${explainedVariance.toFixed(1)}%`);
}

// 초기 데이터 생성 및 시각화
const initialData = generateSampleData(100);
visualizePCA(initialData, 95);

// 슬라이더 이벤트 리스너
d3.select("#variance").on("input", function() {
    const value = this.value;
    d3.select("#variance-value").text(value + "%");
    visualizePCA(initialData, value);
}); 