import * as d3 from "d3";

class RadarChart {
    margin = {
        top: 10, right: 100, bottom: 40, left: 40
    }

    ticks = [60, 80, 100, 120, 140, 160, 180];

    radialScale = d3.scaleLinear()
        .domain([20,180])
        .range([0,250])
    // radialScale = d3.scalePow()
    //     .exponent(0.6)
    //     .domain([0,180])
    //     .range([0,250])
        

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
        this.xAxis = this.svg.append("g");
        this.yAxis = this.svg.append("g");
        this.legend = this.svg.append("g");

        this.xScale = d3.scaleLinear();
        this.yScale = d3.scaleLinear();
        this.zScale = d3.scaleOrdinal().range(d3.schemeCategory10)

        this.svg
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom);

        this.container
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);

        this.line = d3.line()
            .x(d => d.x)
            .y(d => d.y);
        

        // ticks는 고정임 
        // container에다가 추가해야 함 
        this.ticks.forEach(t =>
            this.container.append("circle")
            .attr("cx", 300)
            .attr("cy", 300)
            .attr("fill", "none")
            .attr("stroke", "gray")
            .attr("r", this.radialScale(t))
        );

        this.ticks.forEach(t =>
            this.container.append("text")
            .attr("x", 305)
            .attr("y", 300 - this.radialScale(t))
            .text(t.toString())
        );

        for (let i = 0; i < this.features.length; i++) {
            let ft_name = this.features[i];
            let angle = (Math.PI / 2) + (2 * Math.PI * i / this.features.length);
            // let line_coordinate = this.angleToCoordinate(angle, 10);
            let label_coordinate = this.angleToCoordinate(angle, 200);
    
            //draw axis line
            // this.svg.append("line")
            //     .attr("x1", 300)
            //     .attr("y1", 300)
            //     .attr("x2", line_coordinate.x)
            //     .attr("y2", line_coordinate.y)
            //     .attr("stroke","black");
    
            //draw axis label
            this.container.append("text")
                .attr("x", label_coordinate.x)
                .attr("y", label_coordinate.y)
                .text(ft_name);
        }

        

        

    }

    angleToCoordinate(angle, value){
        let x = Math.cos(angle) * this.radialScale(value);
        let y = Math.sin(angle) * this.radialScale(value);
        return {"x": 300 + x, "y": 300 - y};
    }

    getPathCoordinates(data_point){
        let coordinates = [];
        for (var i = 0; i < this.features.length; i++){
            let ft_name = this.features[i];
            let angle = (Math.PI / 2) + (2 * Math.PI * i / this.features.length);
            coordinates.push(this.angleToCoordinate(angle, data_point[ft_name]));
        }
        return coordinates;
    }

    // https://observablehq.com/@d3/d3-lineradial
    polygon(sides) {
        var length = sides,
          s = 1,
          phase = 0;
        const radial = d3
            .lineRadial()
            .curve(d3.curveLinearClosed)
            .angle((_, i) => (i / length) * 2 * Math.PI + phase)
            .radius(() => s)

          ;
        const poly = function() {
          return radial(Array.from({ length }));
        };
        poly.context = function(_) {
          return arguments.length ? (radial.context(_), poly) : radial.context();
        };
        poly.n = function(_) {
          return arguments.length ? ((length = +_), poly) : length;
        };
        poly.rotate = function(_) {
          return arguments.length ? ((phase = +_), poly) : phase;
        };
        poly.scale = function(_) {
            console.log(arguments)
          return arguments.length ? ((s = +_), poly) : s;
        };
        poly.curve = function(_) {
          return arguments.length ? (radial.curve(_), poly) : radial.curve();
        };
        poly.radius = radial.radius;
        poly.angle = radial.angle;
        return poly;
      }


    update(items){
        console.log('cls', items)
        console.log(items, Array.isArray(items))

        // let colors = ["darkorange", "gray", "navy"];

        // for (let i in items){
        //     let d = items[i];
        //     let color = colors[i];
        //     let coordinates = this.getPathCoordinates(d);

        //     console.log('draw')

        //     console.log(coordinates)

        //     //draw the path element
        //     console.log(this.line)
        //     this.container.append("path")
        //         .datum(coordinates)
        //         .attr("d",this.line)
        //         .attr("stroke-width", 3)
        //         .attr("stroke", color)
        //         .attr("fill", color)
        //         .attr("stroke-opacity", 1)
        //         .attr("opacity", 0.5);
        // }


        // let angleSlice = Math.PI * 2 / 180

        
        let polygon = new this.polygon()
        .curve(d3.curveCardinalClosed)
        .scale(150)
        .n(3)()

        console.log(polygon)

    






        this.container.append("path")
            .attr("transform", `translate(300,300)`) 
            .attr("d", polygon)
            .attr("stroke-width", 3)
            .attr("stroke", 'darkorange')
            .attr("fill", 'darkorange')
            .attr("stroke-opacity", 1)
            .attr("opacity", 0.5);
        

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

