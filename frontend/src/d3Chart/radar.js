import * as d3 from "d3";

class RadarChart {
    margin = {
        top: 100, right: 100, bottom: 100, left: 100
    }

    ticks = [20, 40, 60, 80, 100, 120, 140, 160, 180];

    // radialScale = d3.scaleLinear()
    //    .domain([20,180])
    //    .range([0,200])

    radialScale = d3.scalePow()
    .exponent(0.3)
        .domain([20,180])
        .range([0,200])

        
    line = d3.lineRadial()
            .angle((d) => (Math.PI /3) * d.key)
            .radius((d) => this.radialScale(d.value))
            .curve(d3.curveCardinalClosed)

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
        this.axisAnnotate = this.svg.append("g")
        this.points = this.svg.append("g")

        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);

        this.container
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
        this.axisAnnotate
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
        this.points
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
        

        this.container.selectAll("circle")
            .data(this.ticks)
            .join("circle")
            .attr("cx", this.width / 2)
            .attr("cy", this.height / 2)
            .attr("fill", "gray")
            .attr("fill-opacity", 0.1)
            .attr("stroke", "gray")
            .attr("r", (d) => (this.radialScale(d)))

        this.container.selectAll("text")
            .data(this.ticks)
            .join('text')
            .attr("x", this.width / 2 + 5)
            .attr("y", (d) => (this.height / 2 - this.radialScale(d)))
            .text((d) => (d.toString()))

        this.axisAnnotate.selectAll("text")
            .data(this.features)
            .join('text')
            .attr("x", (d) => this.angleToX(d[1], 220))
            .attr("y", (d) => this.angleToY(d[1], 220))
            .attr("text-anchor", "middle")
            .text((d) => (d[0]));


    }

    angleToX(angle, value){
        let x = Math.cos((Math.PI / 2) + (2 * Math.PI * angle / this.features.length)) * this.radialScale(value)
        return this.width / 2 + x;
    }

    angleToY(angle, value){
        let y =  Math.sin((Math.PI / 2) + (2 * Math.PI * angle / this.features.length)) * this.radialScale(value)
        return this.height / 2 - y ;
    }


    parseStat(item){
        return [
            {
                key : 0, // for angle(radial axis)
                value : item.hp,
                class : 0
            },
            {
                key : 1,
                value : item.attack,
                class : 0
            },
            {
                key : 2,
                value : item.defense,
                class : 0
            },
            {
                key : 3,
                value : item.spattack,
                class : 0
            },
            {
                key : 4,
                value : item.spdefense,
                class : 0
            },            {
                key : 5,
                value : item.speed,
                class : 0
            }
        ]
    }



    update(item, task){

        if (task === "filter"){
            item = item.forEach((i) => this.parseStat(i))
            this.container.selectAll("path")
                .data(item)
                .join("path")
                .transition()
                .attr("transform", `translate(${this.width/2}, ${this.height/2})`)
                .attr("stroke", "#213946")
                .attr("stroke-width", 1)
                .attr('z-index', 200)
                .attr("d", this.line)
                .style("fill-opacity", 0.35)
            this.points.selectAll("circle")
                .data(item)
                .join("circle")
                .transition()
                .attr("transform", `translate(${this.width/2}, ${this.height/2})`)
                .attr("stroke", "#213946")
                .attr("stroke-width", 1)
                .attr('z-index', 200)
                .attr("d", 3)
                .style("fill-opacity", 0.35)

        } else {
            item = [this.parseStat(item)]
            this.container.selectAll("path")
                .data(item)
                .join("path")
                .transition()
                .attr("transform", `translate(${this.width/2}, ${this.height/2})`)
                .attr("stroke", "#213946")
                .attr("stroke-width", 1)
                .attr('z-index', 200)
                .attr("d", this.line)
                .style("fill-opacity", 0.35)
                

            this.points.selectAll("circle")
                .data(item[0])
                .join("circle")
                .transition()
                .attr("cx", (d) => (this.width - this.angleToX(d.key, d.value )))
                .attr("cy", (d) => (this.angleToY(d.key, d.value )))
                .attr("fill", "dark")
                .attr("fill-opacity", 1)
                .attr("stroke", "gray")
                .attr('z-index', 200)
                .attr("r", 3)

        }

        // 영역 안의 background를 만들고
        // 마우스 올라가면 내부를 채우도록 함
        // let blobWrapper = this.container.selectAll(".radarWrapper")
        //     .data(items)
        //     .enter().append("g")
        //     .attr("class", "radarWrapper");

        // blobWrapper
        //     .append("path")
        //     .attr("class", "radarArea")
        //     .attr("d", (d,i) => {i; return radarLine(d); })
        //     .style("fill", (d,i) => {d; return d3.scale.category10().color(i); })
        //     .style("fill-opacity", 0.35)
        //     .on('mouseover', function (d,i){
        //         d;i;
        //         //Dim all blobs
        //         d3.selectAll(".radarArea")
        //             .transition().duration(200)
        //             .style("fill-opacity", 0.1); 
        //         //Bring back the hovered over blob
        //         d3.select(this)
        //             .transition().duration(200)
        //             .style("fill-opacity", 0.7);	
        //     })
        //     .on('mouseout', function(){
        //         //Bring back all blobs
        //         d3.selectAll(".radarArea")
        //             .transition().duration(200)
        //             .style("fill-opacity", 0.35);
        //     });


    }
}


export default RadarChart

