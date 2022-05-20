import * as d3 from "d3";

class RadarChart {
    // reference
    // baseline : https://yangdanny97.github.io/blog/2019/03/01/D3-Spider-Chart
    // tooltip / eventlistener : http://bl.ocks.org/nbremer/21746a9668ffdf6d8242

    margin = {
        top: 50, right: 50, bottom: 50, left: 50
    }

    ticks = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180];

    constructor(svg, features, width = 600, height = 600) {
        this.svg = svg;
        this.features = features;
        this.width = width;
        this.height = height;
        this.handlers = {}; // eventlisteners
    }

    initialize() {
        this.svg = d3.select(this.svg);
        this.container = this.svg.append("g");
        this.axisAnnotate = this.container.append("g")
        this.points = this.container.append("g")
        this.tooltips = this.container.append("g")
        this.highlight = this.container.append("g")

        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);

        this.container
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
            
        this.radialScale = d3.scalePow()
            .exponent(0.8)
            .domain([0,180])
            .range([0,300 * this.width / 600])
    
        this.line = d3.lineRadial()
            .angle(d => (Math.PI /3) * d.key) // key : 0~5 > angle : 0/3 pi ~ 5/3 pi
            .radius(d => this.radialScale(d.value)) 
            .curve(d3.curveCardinalClosed)

        this.container.selectAll("circle")
            .data(this.ticks)
            .join("circle")
            .attr("cx", this.width / 2)
            .attr("cy", this.height / 2)
            .attr("fill", "gray")
            .attr("fill-opacity", 0.1)
            .attr("stroke", "gray")
            .attr("r", d => this.radialScale(d))

        this.container.selectAll("text")
            .data(this.ticks)
            .join('text')
            .style("font-size", "10px")
            .attr("x", this.width / 2 + 5)
            .attr("y", d => this.height / 2 - this.radialScale(d))
            .text(d => d.toString())

        this.axisAnnotate.selectAll("text")
            .data(this.features)
            .join('text')
            .style("font-size", "13px")
            .attr("x", d => this.angleToX(d[1], 2 * this.width / 3 + 20 )) // 300 > 220 2/3 + 20
            .attr("y", d => this.angleToY(d[1], 2 * this.width / 3 + 20))
            .attr("text-anchor", "middle")
            .text(d => d[0]);

        


    }

    angleToX(angle, value){
        // d3's angle starts from zenith
        let x = Math.cos((Math.PI / 2) - (2 * Math.PI * angle / this.features.length)) * this.radialScale(value)
        return this.width / 2 + x;
    }

    angleToY(angle, value){
        let y =  Math.sin((Math.PI / 2) - (2 * Math.PI * angle / this.features.length)) * this.radialScale(value)
        return this.height / 2 - y ;
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

    update(item){
        
        let colors = [item.types[0].color]
        item = [this.parseStat(item)]
        
        // define paths
        let paths = this.container.selectAll("path")
            .data(item)
            .join("path")
        
        // add transition 
        paths
            .transition()
            .attr("transform", `translate(${this.width/2}, ${this.height/2})`)
            .attr("stroke", "#213946")
            .attr("stroke-width", 1)
            .attr('z-index', 200)
            .attr("d", this.line)
            .attr("fill", (d, i) => (colors[i]))
            .style("fill-opacity", 0.5)
        
        // add eventlistener
        paths
            .on('mouseover', (e, d) => {
                e;d;
                //Dim all blobs
                d3.selectAll("path")
                    .transition()
                    .duration(200)
                    .style("fill-opacity", 0.1); 

                this.tooltips.selectAll("text")
                    .data(d)
                    .join('text')
                    .style("font-size", "13px")
                    .attr("x", d => this.angleToX(d.key, d.value + 20)) // 300 > 220 2/3 + 20
                    .attr("y", d => this.angleToY(d.key, d.value  + 20))
                    .attr("text-anchor", "middle")
                    .text(d => d.value);
            })
            .on('mouseout', (d) => {
                d;
                //Bring back all blobs
                d3.selectAll("path")
                    .transition()
                    .duration(200)
                    .style("fill-opacity", 0.35);

                this.tooltips.selectAll("text")
                    .remove()
            });

        this.points.selectAll("circle")
            .data(item.flat())
            .join("circle")
            .transition()
            .attr("cx", d => this.angleToX(d.key, d.value ))
            .attr("cy", d => this.angleToY(d.key, d.value ))
            .attr("fill", "dark")
            .attr("fill-opacity", 1)
            .attr("stroke", "gray")
            .attr('z-index', 200)
            .attr("r", 3)
        

    }
}


export default RadarChart

