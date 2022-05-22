import * as d3 from "d3";

// transition by sort
// https://medium.com/analytics-vidhya/building-racing-bar-chart-in-d3js-d89b71cd3439
class BarChart {
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
        this.rects = this.container.append("g")
        this.focused = this.container.append("g")
        this.tootip = this.container.append("g")

        this.sorted = []

        this.xScale = d3.scaleLinear();
        this.yScale = d3.scaleBand();

        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);

        this.container
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
    }



    sortData(data, order){
        let sorted;
        if (order === "asc"){
            // sorting without dead lock (works like deepcopy)
            sorted = [...data].sort((a,b) => d3.ascending(a.counterCoef, b.counterCoef))
            
        } else if (order ==="desc") {
            sorted = [...data].sort((a,b) => d3.descending(a.counterCoef, b.counterCoef))
        } else {
            sorted = [...data].sort((a,b) => a.types[0].type_index - b.types[0].type_index)
        }
        return sorted
    }


    update(data, order){
        console.log('bar', data)
        // sorted data
        this.sorted = this.sortData(data, order)

        // yScale 
        this.xScale
            .domain([0, d3.max(  data.map( i => i.counterCoef)) + 0.3])
            .range([0, this.width]);
        
        this.yScale
            .domain([...new Set(this.sorted.map(d => d.name))])
            .range([0, this.height])
            .padding(0.3);

        this.xAxis
            .attr("transform", `translate(0, 0)`)
            .call(d3.axisTop(this.xScale))
            .transition()
            
        this.yAxis
            .call(
                d3.axisLeft(this.yScale)
                    .tickFormat((d) => {d; ''})
                    .tickSize(0))
            .transition()

        this.rects.selectAll("rect")
            .data(data)
            .join("rect")
            .transition()
            // move data's x position to sorted data's x position (now criterion is sorted data)
            .attr("x", 0)
            .attr("y", d => this.yScale(this.sorted[this.sorted.findIndex(e => e.name === d.name)].name))
            .attr("height", this.yScale.bandwidth())
            .attr("width", d => this.xScale(d.counterCoef))
            .attr("fill", d => d.types[0].color)
    }


    highlight(highlight){
        console.log('highlight')
        // set opacities of others to 0.1 
        this.rects.selectAll("rect")
            .transition()
            .style("fill-opacity", 0.1)

        // set highlight's opacity to 1 and width 15
        this.focused
            .selectAll("rect")
            .data([highlight])
            .join("rect")
            .attr("x", 0)
            .attr("y", d => this.yScale(this.sorted[this.sorted.findIndex(e => e.name === d.name)].name))
            .attr("height", this.yScale.bandwidth())
            .attr("width", d => this.xScale(d.counterCoef))
            .attr("fill", d => d.types[0].color)
            .style("opacity", 1)

        this.tootip
            .selectAll("text")
            .data([highlight])
            .join("text")
            .style("font-size", "13px")
            .attr("x", d => this.xScale(d.counterCoef) + 5)
            .attr("y", d => this.yScale(this.sorted[this.sorted.findIndex(e => e.name === d.name)].name))
            .attr("text-anchor", "start")
            .attr("alignment-baseline", "hanging")
            .text(d => `${d.name} ${Math.round(d.counterCoef * 100) / 100}`)
    }

    off(){
        this.rects.selectAll("rect")
            .transition()
            .style("fill-opacity", 1)
        this.focused
            .selectAll("rect")
            .remove()
        this.tootip
            .selectAll("text")
            .remove()

    }




}
    



export default BarChart