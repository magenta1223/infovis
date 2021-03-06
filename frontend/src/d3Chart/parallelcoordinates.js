import * as d3 from "d3";

class ParallelCoordinates {
    margin = {
        top: 50, right: 50, bottom: 50, left: 50
    }

    constructor(svg, features, width, height){
        this.svg = svg;
        this.features = features; // statuses 
        this.width = width;
        this.height = height;
    }

    initialize(){
        this.svg = d3.select(this.svg);

        this.xScale = d3.scalePoint()
            .domain(this.features.map(d=>d[0]))
            .range([0, this.width])
        
        this.yScale = d3.scaleLinear()
            .domain([0, 200])
            .range([this.height, 0])
            .clamp(true) // clipping when over the domain range


        this.container = this.svg.append("g");
        this.axes = this.container.append("g");
        this.axisName = this.container.append("g");
        this.lines = this.container.append("g");
        this.focused = this.container.append("g");

        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);


        this.container.attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);

        this.line = (d) => {
            return d3.line()(this.features.map(
                // stat : [statName, statIndex]
                stat => [this.xScale(stat[0]), this.yScale(this.parseStat(d)[stat[1]].value)]
                )
            );
        }

        this.axisName.selectAll("text")
            .data(this.features)
            .join("text")
            .attr("transform", d => `translate(${this.xScale(d[0])}, ${this.height + this.margin.bottom})`)
            .text(d => d[0])
            .attr("text-anchor", "middle")
            .attr("font-size", ".9rem")
            .attr("dy", "-.8rem")

        this.axes.selectAll("g.axis")
            .data(this.features)
            .join("g")
            .attr("class", "axis")
            .attr("transform", d => `translate(${this.xScale(d[0])}, 0)`)
            .each((d, i, nodes) => {
                // all axis share same scales, so only 1st axis needs ticks
                i === 0 ? d3.select(nodes[i]).call(d3.axisLeft(this.yScale)) : d3.select(nodes[i]).call(d3.axisLeft(this.yScale).ticks(0))
            })


    }

    parseStat(item){
        return this.features.map((i) => {
            let stat = i[0].toLowerCase().replace('.', '')
            return {
                key : i[1],
                value : item[stat] ? item[stat] : 0,
                name  : i[0]
            }
        })
    }

    update(data) {

        let colors = data.map(d => d.types[0].color)
        
        this.lines
            .selectAll("path")
            .data(data)
            .join("path")
            .attr("d", this.line)
            .style("fill", "none")
            .style("stroke", (d, i) => (colors[i]))
            .attr("stroke-width", 15)
            .style("opacity", 0.5)


                
    }

    highlight(highlight){
        // color to highlight
        let color = highlight.types[0].color

        // set opacities of others to 0.1 
        this.lines.selectAll("path")
            .transition()
            .style("opacity", 0.1)

        // set highlight's opacity to 1 and width 15
        this.focused
            .selectAll("path")
            .data([highlight])
            .join("path")
            .attr("d", this.line)
            .style("fill", "none")
            .style("stroke", color)
            .style("opacity", 1)
            .attr("stroke-width", 15)
    }

    off(){
        // back to before highlight
        this.lines.selectAll("path")
            .transition()
            .style("opacity", 0.5)
        this.focused
            .selectAll("path")
            .remove()


    }

}

export default ParallelCoordinates