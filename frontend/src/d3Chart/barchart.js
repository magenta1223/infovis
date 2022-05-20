import * as d3 from "d3";
// https://medium.com/analytics-vidhya/building-racing-bar-chart-in-d3js-d89b71cd3439
class BarChart {
    // 타입별 정렬 기능
    // value별 정렬기능
    // 진입 transition
    // 나가는 transition

    margin = {
        top: 50, right: 50, bottom: 50, left: 50
    }
    
    constructor(svg, width, height){
        this.svg = svg
        this.width = width
        this.height = height
    }

    initialize(){
        this.svg = d3.select(this.svg)
        this.container = this.svg.append("g")
        this.xAxis = this.container.append("g");
        this.yAxis = this.container.append("g");
        this.legend = this.container.append("g");
        this.xScale = d3.scaleBand();
        this.yScale = d3.scaleLinear();

        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);

        this.container
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);


        
    }

    update(data, order){
        order;
        // to prevent dead lock
        let copied = JSON.parse(JSON.stringify(data));
        
        if (order === "asc"){
            copied.sort((a,b) => d3.ascending(a.counterCoef, b.counterCoef))
        } else if (order ==="desc") {
            copied.sort((a,b) => d3.descending(a.counterCoef, b.counterCoef))
        } else {
            copied.sort((a,b) => a.types[0].type_index - b.types[0].type_index)
        }
        const categories = [...new Set(copied.map(d => d.name))]

        this.xScale.domain(categories).range([0, this.width]).padding(0.3);
        this.yScale.domain([0, d3.max(  copied.map( i => i.counterCoef)  )]).range([this.height, 0]);

        this.xAxis
            .attr("transform", `translate(0, ${this.height})`)
            .call(d3.axisBottom(this.xScale))
            .transition()
            ;

        this.yAxis
            .call(d3.axisLeft(this.yScale))
            .transition()
            ;

        this.container.selectAll("rect")
            .data(copied)
            .join("rect")
            .attr("x", d => this.xScale(d.name))
            .attr("y", d => this.yScale(d.counterCoef))
            .attr("width", this.xScale.bandwidth())
            .attr("height", d => this.height - this.yScale(d.counterCoef))
            .attr("fill", d => d.types[0].color)
            .transition()



    
    }
}
    



export default BarChart