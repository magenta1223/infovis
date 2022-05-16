import * as d3 from "d3";

class MultiCoordinates {
    margin = {
        top: 50, right: 50, bottom: 10, left: 50
    }

    constructor(svg, features, width, height){
        this.svg = svg;
        console.log(features)
        this.features = features; // statuses 
        this.width = width;
        this.height = height;

        this.selected = ""
    }

    initialize(){
        // labels
        // axes : 모두 같은 scale 이므로 각각 다르게 scale 표시할 필요는 없음
        // 각 item의 primary type별로 coloring을 해주면 됨

        this.svg = d3.select(this.svg);
        this.xScale = d3.scalePoint()
            .domain(this.features.map((d)=>(d[0])))
            .range([0, this.width])

        this.yScale = d3.scaleLinear()
            .domain([0, 200])
            .range([this.height, 0])

        this.container = this.svg.append("g");
        this.axes = this.container.append("g");
        this.titles = this.container.append("g");
        this.lines = this.container.append("g");
        this.focusedLines = this.container.append("g");

        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);


        this.container.attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);

        this.polyline = (d) => {
            return d3.line()(this.features.map(
                (stat) => {
                    // stat : [statName, statIndex]
                    return [this.xScale(stat[0]), this.yScale(this.parseStat(d)[stat[1]].value)]
                })
            );
        }

    }

    parseStat(item){
        return [
            {
                key : 0, // for angle(radial axis)
                value : item.hp ? item.hp : 0,
                name : "HP"
            },
            {
                key : 1,
                value : item.attack ? item.attack : 0,
                name : "ATK"
            },
            {
                key : 2,
                value : item.defense ? item.defense : 0,
                name : "DEF"
            },
            {
                key : 3,
                value : item.spattack ? item.spattack : 0,
                name : "SPATK"
            },
            {
                key : 4,
                value : item.spdefense ? item.spdefense : 0,
                name : "SPDEF"
            },            {
                key : 5,
                value : item.speed ? item.speed : 0,
                name : "SPD"
            }
        ]
    }

    update(data) {

        let colors = data.map((d) => (d.types[0].color))

        console.log('updating ! ')

        console.log( 'x' , this.features[2][0], this.xScale(this.features[2][0]))

        this.axes.selectAll("g.axis")
            .data(this.features)
            .join("g")
            .attr("class", "axis")
            .attr("transform", (d) => `translate(${this.xScale(d[0])}, 0)`)
            .each((d, i, nodes) => {
                // all axis share same scales
                i === 0 ? d3.select(nodes[i]).call(d3.axisLeft(this.yScale)) : d3.select(nodes[i]).call(d3.axisLeft(this.yScale).ticks(0))
            })

        this.titles.selectAll("text")
            .data(this.features)
            .join("text")
            .attr("transform", d => `translate(${this.xScale(d[0])}, 0)`)
            .text(d => d[0])
            .attr("text-anchor", "middle")
            .attr("font-size", ".9rem")
            .attr("dy", "-.8rem")

        this.lines
            .selectAll("path")
            .data(data)
            .join("path")
            .attr("d", this.polyline)
            .style("fill", "none")
            .style("stroke", (d, i) => (colors[i]))
            .attr("stroke-width", 15)
            .style("opacity", 0.5)
            .on("click", (e,d) => {
                this.highlight(d)
            })

                
    }

    highlight(highlight){
        highlight;
        console.log('highlight',highlight)
        let color = highlight.types[0].color

        this.lines.selectAll("path")
            .transition(30)
            .style("opacity", 0.1)

    
        this.focusedLines
            .selectAll("path")
            .data([highlight])
            .join("path")
            .attr("d", this.polyline)
            .style("fill", "none")
            .style("stroke", color)
            .style("opacity", 1)
            .attr("stroke-width", 15)

        this.selected  = highlight
        
    }
}

export default MultiCoordinates