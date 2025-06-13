// D3.js 3D 지구(orthographic projection) + 광물 위치 시각화

const width = 600;
const height = 600;
const globeSvg = d3.select("#globe");
const tooltip = d3.select("#tooltip");

// 투영법 설정 (orthographic: 3D 구처럼 보임)
const projection = d3.geoOrthographic()
    .scale(280)
    .translate([width / 2, height / 2])
    .clipAngle(90);

const path = d3.geoPath().projection(projection);

// 지구 회전 변수
let rotation = {lambda: 0, phi: 0};
let isDragging = false;
let lastPos = null;

// 지도 데이터 로드 (world-atlas)
Promise.all([
    d3.json("https://unpkg.com/world-atlas@2.0.2/countries-110m.json"),
    d3.json("minerals.json")
]).then(([world, minerals]) => {
    const countries = topojson.feature(world, world.objects.countries);

    // 지구 그리기
    globeSvg.append("circle")
        .attr("cx", width / 2)
        .attr("cy", height / 2)
        .attr("r", projection.scale())
        .attr("fill", "#b3d1e7");

    globeSvg.append("g")
        .selectAll("path")
        .data(countries.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("fill", "#e0e7ef")
        .attr("stroke", "#888");

    // 광물 리스트 UI
    const mineralsDiv = d3.select("#minerals");
    minerals.forEach((mineral, idx) => {
        mineralsDiv.append("button")
            .attr("class", "mineral-btn")
            .attr("id", `mineral-btn-${idx}`)
            .text(mineral.name)
            .on("click", () => showMineral(mineral));
    });

    // 마커 그룹
    const markerGroup = globeSvg.append("g");

    // 광물 클릭 시 마커 표시
    function showMineral(mineral) {
        markerGroup.selectAll("circle").remove();
        markerGroup.selectAll("circle")
            .data(mineral.locations)
            .enter()
            .append("circle")
            .attr("cx", d => projection([d.lon, d.lat])[0])
            .attr("cy", d => projection([d.lon, d.lat])[1])
            .attr("r", 8)
            .attr("fill", "#f7b32b")
            .attr("stroke", "#333")
            .attr("stroke-width", 2)
            .on("mouseover", function(event, d) {
                tooltip.style("opacity", 1)
                    .html(`<b>${mineral.name}</b><br>${d.desc}<br>위도: ${d.lat}<br>경도: ${d.lon}`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 30) + "px");
            })
            .on("mouseout", function() {
                tooltip.style("opacity", 0);
            });
    }

    // 드래그로 지구 회전
    globeSvg.call(d3.drag()
        .on("start", (event) => {
            isDragging = true;
            lastPos = [event.x, event.y];
        })
        .on("drag", (event) => {
            if (!isDragging) return;
            const dx = event.x - lastPos[0];
            const dy = event.y - lastPos[1];
            rotation.lambda += dx * 0.5;
            rotation.phi -= dy * 0.5;
            projection.rotate([rotation.lambda, rotation.phi]);
            globeSvg.selectAll("path").attr("d", path);
            globeSvg.selectAll("circle").attr("cx", d => projection([d.lon, d.lat])[0])
                                         .attr("cy", d => projection([d.lon, d.lat])[1]);
            lastPos = [event.x, event.y];
        })
        .on("end", () => {
            isDragging = false;
        })
    );

    // 초기 첫 번째 광물 표시
    showMineral(minerals[0]);
}); 