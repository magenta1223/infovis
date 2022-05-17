import * as d3 from "d3";

class SunBurst {
    margin = {
        top: 50, right: 50, bottom: 50, left: 50
    }
    
    constructor(svg, width, height){
        this.svg = svg
        this.width = width
        this.height = height
        this.radius = Math.min(width, height) / 2;

    }

    initialize(){
        this.svg = d3.select(this.svg)
        this.container = this.svg.append("g")

        this.svg
            .attr("width", this.width)
            .attr("height", this.height)

        this.container
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
        
        // 아마도 arc partition
        this.partition = d3.partition()
            .size([2 * Math.PI, this.radius * this.radius]) // 
            //.value((d) => (d.size) );

        this.arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
            .padRadius(this.radius * 1.5)
            .innerRadius(d => d.y0 * this.radius)
            .outerRadius(d => Math.max(d.y0 * this.radius, d.y1 * this.radius - 1))

        this.container.append("circle")
            .attr("r", this.radius)
            .style("opacity", 0);
        
        this.colors = {
            "VeryHigh": "#0052cc",
            "High": "#00b85c",
            "Moderate": "#ff9900",
            "Low": "#e6e600",
            "Supplemental": "#c2f0ff",
            "NA": "#cccccc"
          };
    }

    partition(data){
        let root = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);
        console.log('root', root)
        return d3.partition().size([2 * Math.PI, root.height + 1])(root);
    }

    arcVisible(d){
        return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0
    }
    
    labelVisible(d) {
        return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
    }
    
    labelTransform(d) {
        const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
        const y = (d.y0 + d.y1) / 2 * this.radius;
        return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
    }


    update(data){

        let color = d3.scaleOrdinal(d3.quantize(d3.interpolateRgbBasis(["#FFC917", "#FE6200", "#00AA89", "#0079D3", "#003082","#6C59B1"]), data.children.length ))
        let format = d3.format(",d")

        let root = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);

        root = d3.partition().size([2 * Math.PI, root.height + 1])(root)

        //let root = this.partition(data)

        root.each(d => d.current = d);

        const path = this.container.append("g")
            .selectAll("path")
            .data(root.descendants().slice(1))
            .join("path")
            .attr("fill", d => { while (d.depth > 1) d = d.parent; return color(d.data.name); })
            .attr("fill-opacity", d => this.arcVisible(d.current) ? (d.children ? 0.7 : 0.4) : 0)
            .attr("pointer-events", d => this.arcVisible(d.current) ? "auto" : "none")
            .attr("d", d => this.arc(d.current));

        
        
        // const label = this.container.append("g")
        //     .attr("pointer-events", "none")
        //     .attr("text-anchor", "middle")
        //     .style("user-select", "none")
        //     .selectAll("text")
        //     .data(root.descendants().slice(1))
        //     .join("text")
        //     .attr("dy", "0.35em")
        //     .attr("style","fill: #fff; stroke: #000; stroke-width:3px; paint-order: stroke fill;")
        //     .attr("fill-opacity", d => +this.labelVisible(d.current))
        //     .attr("stroke-opacity", d => +this.labelVisible(d.current))
        //     .attr("transform", d => this.labelTransform(d.current))
        //     .text(d => d.data.name);


        



    

        
        
    }
    
    // title달기. 필요 없음
    // sysName = json.sysName;
    // var titletext = sysName + " - Impact to Organization";
    // d3.select("#title2").text(titletext);

    // 몰라
    // initializeBreadcrumbTrail();
    // 이전 차트 초기화. 필요 업슴
    // d3.select("#chart svg").remove();
    
    // done in initialize
    // var vis = d3.select("#chart").append("svg:svg")
    //   .attr("width", width)
    //   .attr("height", height)
    //   .append("svg:g")
    //   .attr("id", "container")
    //   .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    // var partition = d3.layout.partition()
    //   .size([2 * Math.PI, radius * radius])
    //   .value(function(d) { return d.size; });
    // var arc = d3.svg.arc()
    //   .startAngle(function(d) { return d.x; })
    //   .endAngle(function(d) { return d.x + d.dx; })
    //   .innerRadius(function(d) { return Math.sqrt(d.y); })
    //   .outerRadius(function(d) { return Math.sqrt(d.y + d.dy);  });
    // Bounding circle underneath the sunburst, to make it easier to detect when the mouse leaves the parent g.
    // vis.append("svg:circle")
    //     .attr("r", radius)
    //     .style("opacity", 0);
     // For efficiency, filter nodes to keep only those large enough to see.
    // var nodes = partition.nodes(json)
    //    .filter(function(d) {
    //     return (d.dx > 0.005); // 0.005 radians = 0.29 degrees
    //     });
    //  var path = vis.data([json]).selectAll("path")
    //     .data(nodes)
    //     .enter().append("svg:path")
    //     .attr("display", function(d) { return d.depth ? null : "none"; })
    //     .attr("d", arc)
    //     .attr("fill-rule", "evenodd")
    //     .style("fill", function(d) { return colors[d.category]; })
    //     .style("opacity", 1)
    //     .on("mouseover", mouseover);
    //    // Add the mouseleave handler to the bounding circle.
    // d3.select("#container").on("mouseleave", mouseleave);
    // // Get total size of the tree = value of root node from partition.
    // totalSize = path.node().__data__.value;
    // path.exit().remove();
    // nodes.exit().remove();
    // arc.exit().remove();
    // partition.exit().remove();
    // vis.exit().remove();
  }



// (data, { // data is either tabular (array of objects) or hierarchy (nested objects)
//     path, // as an alternative to id and parentId, returns an array identifier, imputing internal nodes
//     id = Array.isArray(data) ? d => d.id : null, // if tabular data, given a d in data, returns a unique identifier (string)
//     parentId = Array.isArray(data) ? d => d.parentId : null, // if tabular data, given a node d, returns its parent’s identifier
//     children, // if hierarchical data, given a d in data, returns its children
//     value, // given a node d, returns a quantitative value (for area encoding; null for count)
//     sort = (a, b) => d3.descending(a.value, b.value), // how to sort nodes prior to layout
//     label, // given a node d, returns the name to display on the rectangle
//     title, // node가 d로 주어졌을 때 상위 노드의 이름 반환. 아마도 grouping 때문에 그런듯..  
//     link, // given a node d, its link (if any)
//     linkTarget = "_blank", // the target attribute for links (if any)


//     padding = 1, // separation between arcs
//     radius = Math.min(width - marginLeft - marginRight, height - marginTop - marginBottom) / 2, // outer radius
//     color = d3.interpolateRainbow, // color scheme, if any
//     fill = "#ccc", // fill for arcs (if no color encoding)
//     fillOpacity = 0.6, // fill opacity for arcs
//   } = {}) {
  
//     // If id and parentId options are specified, or the path option, use d3.stratify
//     // to convert tabular data to a hierarchy; otherwise we assume that the data is
//     // specified as an object {children} with nested objects (a.k.a. the “flare.json”
//     // format), and use d3.hierarchy.
//     const root = path != null ? d3.stratify().path(path)(data)
//         : id != null || parentId != null ? d3.stratify().id(id).parentId(parentId)(data)
//         : d3.hierarchy(data, children);
  
//     // Compute the values of internal nodes by aggregating from the leaves.
//     value == null ? root.count() : root.sum(d => Math.max(0, value(d)));
  
//     // Sort the leaves (typically by descending value for a pleasing layout).
//     if (sort != null) root.sort(sort);
  
//     // Compute the partition layout. Note polar coordinates: x is angle and y is radius.
//     d3.partition().size([2 * Math.PI, radius])(root);
  
//     // Construct a color scale.
//     if (color != null) {
//       color = d3.scaleSequential([0, root.children.length - 1], color).unknown(fill);
//       root.children.forEach((child, i) => child.index = i);
//     }
  
//     // Construct an arc generator.
//     const arc = d3.arc()
//         .startAngle(d => d.x0)
//         .endAngle(d => d.x1)
//         .padAngle(d => Math.min((d.x1 - d.x0) / 2, 2 * padding / radius))
//         .padRadius(radius / 2)
//         .innerRadius(d => d.y0)
//         .outerRadius(d => d.y1 - padding);
  
//     const svg = d3.create("svg")
//         .attr("viewBox", [
//           marginRight - marginLeft - width / 2,
//           marginBottom - marginTop - height / 2,
//           width,
//           height
//         ])
//         .attr("width", width)
//         .attr("height", height)
//         .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
//         .attr("font-family", "sans-serif")
//         .attr("font-size", 10)
//         .attr("text-anchor", "middle");
  
//     const cell = svg
//       .selectAll("a")
//       .data(root.descendants())
//       .join("a")
//         .attr("xlink:href", link == null ? null : d => link(d.data, d))
//         .attr("target", link == null ? null : linkTarget);
  
//     cell.append("path")
//         .attr("d", arc)
//         .attr("fill", color ? d => color(d.ancestors().reverse()[1]?.index) : fill)
//         .attr("fill-opacity", fillOpacity);
  
//     if (label != null) cell
//       .filter(d => (d.y0 + d.y1) / 2 * (d.x1 - d.x0) > 10)
//       .append("text")
//         .attr("transform", d => {
//           if (!d.depth) return;
//           const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
//           const y = (d.y0 + d.y1) / 2;
//           return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
//         })
//         .attr("dy", "0.32em")
//         .text(d => label(d.data, d));
  
//     if (title != null) cell.append("title")
//         .text(d => title(d.data, d));
  
//     return svg.node();
//   }


export default SunBurst