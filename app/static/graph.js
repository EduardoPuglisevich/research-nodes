// Selecciona el elemento SVG y define el tamaño
const svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

// Selecciona el tooltip
const tooltip = d3.select("#tooltip");

// Configura las fuerzas para los nodos y enlaces
const simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));

// Agrega las líneas de los enlaces
const link = svg.append("g")
    .selectAll("line")
    .data(links)
    .enter().append("line")
    .attr("class", "link");

// Agrega los nodos como círculos y configura el tooltip
const node = svg.append("g")
    .selectAll("circle")
    .data(nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", 8)
    .attr("fill", d => d3.schemeCategory10[d.group])
    .on("mouseover", (event, d) => {
        tooltip
            .style("visibility", "visible")
            .text(`ID: ${d.id}, Comunidad: ${d.group}`);
    })
    .on("mousemove", (event) => {
        tooltip
            .style("top", (event.pageY + 5) + "px")
            .style("left", (event.pageX + 5) + "px");
    })
    .on("mouseout", () => {
        tooltip.style("visibility", "hidden");
    });

// Agrega etiquetas de arrastre a los nodos
node.call(d3.drag()
    .on("start", dragStarted)
    .on("drag", dragged)
    .on("end", dragEnded));

// Ejecuta la simulación
simulation.nodes(nodes).on("tick", ticked);
simulation.force("link").links(links);

function ticked() {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
}

// Funciones de arrastre
function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}
