import * as d3 from "d3";



import { createPopper } from '@popperjs/core';

createPopper;
class RadarChart {
    // reference
    // baseline : https://yangdanny97.github.io/blog/2019/03/01/D3-Spider-Chart
    // tooltip / eventlistener : http://bl.ocks.org/nbremer/21746a9668ffdf6d8242

    margin = {
        top: 60, right: 60, bottom: 60, left: 60
    }

    ticks = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180];


    constructor(svg, features, width = 600, height = 600) {
        this.svg = svg;
        this.features = features;
        this.width = width;
        this.height = height;
        this.tooltipids = ["#t0", "#t1", "#t2", "#t3", "#t4", "#t5"]
    }

    initialize() {
        this.svg = d3.select(this.svg)
        // container
        this.container = this.svg.append("g")
        
        this.axisAnnotate = this.container.append("g")

        // popper reference point
        this.center = this.container.append("g")
        this.points = this.container.append("g")
        this.highlight = this.container.append("g")
        this.total = d3.select("#t7")


        this.tooltips = []

        for (let i in this.tooltipids){
            this.tooltips.push(d3.select(this.tooltipids[i]))
        }


        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);

        this.container
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
        
        this.radialScale = d3.scalePow()
            .exponent(0.8)
            .domain([0,180])
            .range([0,300 * this.width / 600])
            .clamp(true) // clipping when over the domain range
    
        // degree to radian
        this.line = d3.lineRadial()
            .angle(d => (Math.PI /3) * d.key) // // degree to radian. key : 0~5 > angle : 0/3 pi ~ 5/3 pi
            .radius(d => this.radialScale(d.value)) 
            .curve(d3.curveCardinalClosed)

        // concentric circles
        this.container.selectAll("circle")
            .data(this.ticks)
            .join("circle")
            .attr("cx", this.width / 2)
            .attr("cy", this.height / 2)
            .attr("fill", "gray")
            .attr("fill-opacity", 0.1)
            .attr("stroke", "gray")
            .attr("r", d => this.radialScale(d))


        this.axisAnnotate.selectAll("text")
            .data(this.features)
            .join('text')
            .style("font-size", "13px")
            .attr("x", d => this.angleToX(d[1], 2 * this.width / 3 + 100 )) // 300 > 220 2/3 + 20
            .attr("y", d => this.angleToY(d[1], 2 * this.width / 3 + 100))
            .attr("text-anchor", "middle")
            .text(d => d[0]);

        this.center.selectAll("circle")
            .data([0])
            .join("circle")
            .attr("cx", this.width / 2)
            .attr("cy", this.height / 2)
            .attr("r", 0)

        


    }
    
    // polar coordinates to orthogonal coordinate 
    angleToX(angle, value){
        // d3's angle starts from zenith
        let x = Math.cos((Math.PI / 2) - (2 * Math.PI * angle / this.features.length)) * this.radialScale(value)
        return this.width / 2 + x;
    }

    // polar coordinates to orthogonal coordinate
    angleToY(angle, value){
        let y =  Math.sin((Math.PI / 2) - (2 * Math.PI * angle / this.features.length)) * this.radialScale(value)
        return this.height / 2 - y ;
    }
    
    // parse item for radar chart
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
        // for .data()
        item = [this.parseStat(item)]
        
        // define paths
        let paths = this.container.selectAll("path")
            .data(item)
            .join("path")
        
            paths
            .on('mouseover', (e, d) => {
                // text tooltip

                // highlight the area
                d3.selectAll("path")
                    .transition()
                    .duration(200)
                    .style("fill-opacity", 0.8); 

                console.log(this.center.select("circle")._groups[0][0])
                    
                for (let i in this.tooltips){

                    this.tooltips[i]
                        .selectAll(".tooltip")
                        .html(d[i].value)
                        .style("visibility", "visible")

                    createPopper(this.center.select("circle")._groups[0][0], this.tooltips[i].node(), {
                        placement : "bottom",
                        modifiers : [
                            {
                                name : "offset",
                                options : {
                                    offset : [this.angleToX(d[i].key, d[i].value + 50) - this.width / 2, this.angleToY(d[i].key, d[i].value + 50) - this.height / 2 - 15]
                                }
                            }
                        ]
                    });

                    // popper for vue
                    // https://vuecomponent.com/integrations/popperjs.html

                }

                let sum = 0

                d.forEach(e => {
                    sum += e.value
                });

                this.total
                    .selectAll(".tooltip")
                    .html("total " + sum)
                    .style("visibility", "visible")

                createPopper(this.center.select("circle")._groups[0][0], this.total.node(), {
                    placement : "bottom",
                    modifiers : [
                        {
                            name : "offset",
                            options : {
                                offset : [0, -15]
                            }
                        }
                    ]
                });



                
                // lower the opacity of text
                this.axisAnnotate.selectAll("text")
                    .style('opacity', 0.2)
                    
            })
            .on('mouseout', (d) => {
                d;
                // bring back
                d3.selectAll("path")
                    .transition()
                    .duration(200)
                    .style("fill-opacity", 0.35);

                this.axisAnnotate.selectAll("text")
                    .style('opacity', 1)

                for (let i in this.tooltips){
                    this.tooltips[i]
                    .selectAll(".tooltip")
                        .style("visibility", "hidden")
                }

                this.total.selectAll(".tooltip")
                    .style("visibility", "hidden")

            });


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
        
        
        // points for stat (redundant encoding)
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

