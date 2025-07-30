function verEquipos(liga) {
    console.log("Éxito");
    const equiposPorLiga = {
        premier: {
        nombre: "Premier League",
        equipos: [
            { nombre: "Manchester City", imagenes: "static/imagenes/Ligas/PremierLeague/ManchesterCity/manchester-city.png", id: "1" },
            { nombre: "Manchester United", imagenes: "static/imagenes/Ligas/PremierLeague/ManchesterUnited/manchester-united.png", id: "2" },
            { nombre: "Liverpool", imagenes: "static/imagenes/Ligas/PremierLeague/Liverpool/liverpool.png", id: "4" },
            { nombre: "Arsenal", imagenes: "static/imagenes/Ligas/PremierLeague/Arsenal/arsenal.png", id: "3" },
            { nombre: "Chelsea", imagenes: "static/imagenes/Ligas/PremierLeague/Chelsea/chelsea.png", id: "5" },
            { nombre: "Tottenham", imagenes: "static/imagenes/Ligas/PremierLeague/Tottenham/tottenham.png", id: "6" },
        ]
        },
        laliga: {
        nombre: "La Liga",
        equipos: [
            { nombre: "Real Madrid", imagenes: "static/imagenes/Ligas/LaLiga/RealMadrid/real-madrid.png", id: "7" },
            { nombre: "Barcelona", imagenes: "static/imagenes/Ligas/LaLiga/Barcelona/barcelona.png", id: "8" },
            { nombre: "Atlético de Madrid", imagenes: "static/imagenes/Ligas/LaLiga/AtleticoMadrid/atletico-madrid.png", id: "11" },
            { nombre: "Sevilla", imagenes: "static/imagenes/Ligas/LaLiga/Sevilla/sevilla.png", id: "9" },
            { nombre: "Athletic Club", imagenes: "static/imagenes/Ligas/LaLiga/AthleticBilbao/athletic-bilbao.png", id: "10" },
            { nombre: "Villarreal", imagenes: "static/imagenes/Ligas/LaLiga/Villarreal/villarreal.png", id: "12" },
        ]
        },
        bundesliga: {
        nombre: "Bundesliga",
        equipos: [
            { nombre: "Bayern Múnich", imagenes: "static/imagenes/Ligas/Bundesliga/BayernMunich/bayern-munich.png", id: "13" },
            { nombre: "Borussia Dortmund", imagenes: "static/imagenes/Ligas/Bundesliga/BorussiaDortmund/borussia-dortmund.png", id: "15" },
            { nombre: "RB Leipzig", imagenes: "static/imagenes/Ligas/Bundesliga/Leipzig/rb-leipzig.png", id: "16" },
            { nombre: "Bayer Leverkusen", imagenes: "static/imagenes/Ligas/Bundesliga/BayerLeverkusen/bayer-leverkusen.png", id: "14" },
            { nombre: "Eintracht Frankfurt", imagenes: "static/imagenes/Ligas/Bundesliga/EintrachtFrankfurt/eintracht-frankfurt.png", id: "17" },
            { nombre: "Wolfsburgo", imagenes: "static/imagenes/Ligas/Bundesliga/Wolfsburgo/wolfsburgo.png", id: "18" },
        ]
        },
        seriea: {
        nombre: "Serie A",
        equipos: [
            { nombre: "Juventus", imagenes: "static/imagenes/Ligas/SerieA/Juventus/juventus.png", id: "19" },
            { nombre: "AC Milan", imagenes: "static/imagenes/Ligas/SerieA/AcMilan/ac-milan.png", id: "21" },
            { nombre: "Inter de Milan", imagenes: "static/imagenes/Ligas/SerieA/InterMilan/inter-milan.png", id: "23" },
            { nombre: "Napoli", imagenes: "static/imagenes/Ligas/SerieA/Napoli/napoli.png", id: "20" },
            { nombre: "Roma", imagenes: "static/imagenes/Ligas/SerieA/Roma/roma.png", id: "22" },
            { nombre: "Lazio", imagenes: "static/imagenes/Ligas/SerieA/Lazio/lazio.png", id: "24" },
        ]
        },
        ligue1: {
        nombre: "Ligue 1",
        equipos: [
            { nombre: "PSG", imagenes: "static/imagenes/Ligas/Ligue1/PSG/psg.png", id: "25" },
            { nombre: "Olympique Lyon", imagenes: "static/imagenes/Ligas/Ligue1/OlympiqueLyon/olympique-lyon.png", id: "28" },
            { nombre: "Olympique Marsella", imagenes: "static/imagenes/Ligas/Ligue1/OlympiqueMarsella/olympique-marsella.png", id: "29" },
            { nombre: "Lille", imagenes: "static/imagenes/Ligas/Ligue1/Lille/lille.png", id: "26" },
            { nombre: "Monaco", imagenes: "static/imagenes/Ligas/Ligue1/ASMonaco/monaco.png", id: "27" },
            { nombre: "Stade Rennes", imagenes: "static/imagenes/Ligas/Ligue1/Rennes/rennes.png", id: "30" },
        ]
        }
    };

    const contenedor = document.getElementById('contenedor-equipos');
    contenedor.innerHTML = ""; // Limpiar contenido anterior

    if (equiposPorLiga[liga]) {
        equiposPorLiga[liga].equipos.forEach(equipo => {
        const col = document.createElement('div');
        col.className = 'col text-center';

        col.innerHTML = `
            <img src="${equipo.imagenes}" alt="${equipo.nombre}" class="img-fluid rounded shadow-sm equipo-img" 
                style="max-height: 100px; cursor: pointer;" 
                onclick="verJugadores('${liga}', '${equipo.id}')">
            <p class="mt-2">${equipo.nombre}</p>
        `;
        contenedor.appendChild(col);
        });

        // Actualiza el título del modal
        document.getElementById('equiposModalLabel').textContent = `Equipos de la ${liga.toUpperCase()}`;

        // Mostrar el modal usando Bootstrap
        const modal = new bootstrap.Modal(document.getElementById('equiposModal'));
        modal.show();
    } else {
        alert("No se encontraron equipos para la liga: " + liga);
    }
}

// function verJugadores(liga, equipo) {
//     const jugadoresPorEquipo = {
//         "Manchester City": [
//         { nombre: "Erling Haaland", edad: 23, img: "static/img/Jugadores/Haaland.png" },
//         { nombre: "Kevin De Bruyne", edad: 32, img: "static/img/Jugadores/DeBruyne.png" }
//         ],
//         "Real Madrid": [
//         { nombre: "Jude Bellingham", edad: 20, img: "static/img/Jugadores/Bellingham.png" },
//         { nombre: "Vinícius Jr", edad: 23, img: "static/img/Jugadores/Vinicius.png" }
//         ],
//         // Agrega los demás equipos aquí
//     };

//     const jugadores = jugadoresPorEquipo[equipo];
//     const contenedor = document.getElementById('contenedor-jugadores');
//     contenedor.innerHTML = ""; // Limpiar

//     if (jugadores && jugadores.length > 0) {
//         jugadores.forEach(jugador => {
//         const item = document.createElement('div');
//         item.className = 'list-group-item d-flex align-items-center';

//         item.innerHTML = `
//             <img src="${jugador.img}" alt="${jugador.nombre}" class="rounded me-3" style="width: 50px; height: 50px;" />
//             <div>
//                 <strong>${jugador.nombre}</strong><br />
//                 <small>Edad: ${jugador.edad}</small>
//             </div>
//         `;

//         contenedor.appendChild(item);
//         });

//         document.getElementById('jugadoresModalLabel').textContent = `Jugadores de ${equipo}`;

//         const jugadoresModal = new bootstrap.Modal(document.getElementById('jugadoresModal'));
//         jugadoresModal.show();
//     } else {
//         alert(`No se encontraron jugadores para ${equipo}`);
//     }
// }

function verJugadores(liga, equipoId) {
    $.ajax({
        url: '/obtener_jugadores_por_equipo/',
        type: 'GET',
        data: { equipo_id: equipoId },
        success: function(jugadores) {
            const contenedor = document.getElementById('contenedor-jugadores');
            contenedor.innerHTML = ""; // Limpiar

            if (jugadores && jugadores.length > 0) {
                jugadores.forEach(jugador => {
                    // Corregir ruta para evitar doble slash
                    const rutaImg = jugador.img.startsWith('/')
                        ? `/static${jugador.img}`
                        : `/static/${jugador.img}`;

                    const item = document.createElement('div');
                    item.className = 'list-group-item d-flex align-items-center';
                    item.innerHTML = `
                        <a href="/jugador/${jugador.id}" style="text-decoration: none; color: inherit;">
                            <img src="${rutaImg}" alt="${jugador.nombre}" class="rounded me-3" style="width: 50px; height: 60px;" />
                            <div>
                                <strong>${jugador.nombre}</strong><br />
                                <small>Edad: ${jugador.edad}</small>
                            </div>
                        </a>
                    `;
                    contenedor.appendChild(item);
                });

                document.getElementById('jugadoresModalLabel').textContent = `Jugadores del equipo`;
                const jugadoresModal = new bootstrap.Modal(document.getElementById('jugadoresModal'));
                jugadoresModal.show();
            } else {
                alert("No se encontraron jugadores para este equipo.");
            }
        },
        error: function(xhr, status, error) {
            alert("Error al consultar los jugadores.");
            console.error("Error:", error);
        }
    });
}


function ocultar(){
    $("#PaginaM").innerHTML("");
}

function mostrarToast(mensaje) {
    $("#toast-mensaje").text(mensaje);
    const toast = new bootstrap.Toast(document.getElementById('toast-alerta'));
    toast.show();
}

function consultarSolicitudes() {
    event.preventDefault(); // Evita que recargue la página

    const desde = $("#desde").val();
    const hasta = $("#hasta").val();

    // Validación
    if (!desde || !hasta) {
        mostrarToast("Ambas fechas son obligatorias.");
        return;
    }

    if (desde > hasta) {
        mostrarToast("La fecha 'Desde' no puede ser mayor que la fecha 'Hasta'.");
        return;
    }

    // Si todo está bien, realiza la consulta
    $.ajax({
        url: `/obtener_solicitudes/`,
        type: 'GET',
        data: {
            desde: desde,
            hasta: hasta
        },
        success: function(data) {
            const $tabla = $("#tabla_registros");
            $tabla.empty();

            if (data.length === 0) {
                $tabla.append(`<tr><td colspan="5" class="text-center">No se encontraron registros.</td></tr>`);
                return;
            }

            data.forEach(function(solicitud) {
                const row = `
                    <tr>
                        <td>${solicitud.usuario}</td>
                        <td>${solicitud.jugador}</td>
                        <td>${solicitud.mensaje}</td>
                        <td>${solicitud.estado}</td>
                        <td>${solicitud.fecha}</td>
                    </tr>`;
                $tabla.append(row);
            });
        },
        error: function(xhr, status, error) {
            mostrarToast("Error al consultar las solicitudes.");
            console.error("Error al consultar:", error);
        }
    });
}

function consultarSolicitudesAprobadas() {
    event.preventDefault();

    const desde = $("#desde").val();
    const hasta = $("#hasta").val();

    if (!desde || !hasta) {
        mostrarToast("Ambas fechas son obligatorias.");
        return;
    }

    if (desde > hasta) {
        mostrarToast("La fecha 'Desde' no puede ser mayor que la fecha 'Hasta'.");
        return;
    }

    $.ajax({
        url: `/obtener_solicitudes_aprobadas/`,
        type: 'GET',
        data: {
            desde: desde,
            hasta: hasta
        },
        success: function(data) {
            const $tabla = $("#tabla_registros_aprobadas");
            $tabla.empty();

            if (data.length === 0) {
                $tabla.append(`<tr><td colspan="3" class="text-center">No se encontraron registros.</td></tr>`);
                return;
            }

            data.forEach(function(solicitud) {
                const row = `
                    <tr>
                        <td>${solicitud.total}</td>
                        <td>${solicitud.fecha}</td>
                        <td>${solicitud.estado}</td>
                    </tr>`;
                $tabla.append(row);
            });
        },
        error: function(xhr, status, error) {
            mostrarToast("Error al consultar las solicitudes aprobadas.");
            console.error("Error:", error);
        }
    });
}


function consultarUsuariosRegistrados() {
    event.preventDefault();

    const desde = $("#desde").val();
    const hasta = $("#hasta").val();

    if (!desde || !hasta) {
        mostrarToast("Ambas fechas son obligatorias.");
        return;
    }

    if (desde > hasta) {
        mostrarToast("La fecha 'Desde' no puede ser mayor que la fecha 'Hasta'.");
        return;
    }

    $.ajax({
        url: `/obtener_usuarios_registrados/`,
        type: 'GET',
        data: {
            desde: desde,
            hasta: hasta
        },
        success: function(data) {
            const $tabla = $("#tabla_usuarios");
            $tabla.empty();

            if (data.length === 0) {
                $tabla.append(`<tr><td colspan="4" class="text-center">No se encontraron registros.</td></tr>`);
                return;
            }

            data.forEach(function(usuario) {
                const row = `
                    <tr>
                        <td>${usuario.nombre}</td>
                        <td>${usuario.tipo}</td>
                        <td>${usuario.fecha}</td>
                    </tr>`;
                $tabla.append(row);
            });
        },
        error: function(xhr, status, error) {
            mostrarToast("Error al consultar los usuarios registrados.");
            console.error("Error:", error);
        }
    });
}


function consultarSolicitudesSemanales() {
    event.preventDefault();

    const desde = $("#desde").val();
    const hasta = $("#hasta").val();

    if (!desde || !hasta) {
        mostrarToast("Ambas fechas son obligatorias.");
        return;
    }

    if (desde > hasta) {
        mostrarToast("La fecha 'Desde' no puede ser mayor que la fecha 'Hasta'.");
        return;
    }

    $.ajax({
        url: `/obtener_solicitudes_semanales/`,
        type: 'GET',
        data: {
            desde: desde,
            hasta: hasta
        },
        success: function(data) {
            const $tabla = $("#tabla_semanal");
            $tabla.empty();

            if (data.length === 0) {
                $tabla.append(`<tr><td colspan="3" class="text-center">No se encontraron registros.</td></tr>`);
                return;
            }

            data.forEach(function(registro) {
                const row = `
                    <tr>
                        <td>${registro.semana}</td>
                        <td>${registro.anio}</td>
                        <td>${registro.total}</td>
                    </tr>`;
                $tabla.append(row);
            });
        },
        error: function(xhr, status, error) {
            mostrarToast("Error al consultar las solicitudes semanales.");
            console.error("Error:", error);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const selectReporte = document.getElementById("tipo_reporte");
    const topNInput = document.getElementById("top_n_input");

    selectReporte.addEventListener("change", function () {
        const selected = this.value;
        // Mostrar input si es "nacionalidades"
        if (selected === "nacionalidades") {
            document.getElementById("parametros_extra").style.display = "flex";
            topNInput.style.display = "block";
        } else {
            topNInput.style.display = "none";
            document.getElementById("parametros_extra").style.display = "none";
        }
    });

    document.getElementById("btn-generar").addEventListener("click", generarGrafica);
});



window.generarGrafica = function () {
    const tipo = document.getElementById("tipo_reporte").value;
    if (!tipo) return;

    let url = `/reporte_datos/${tipo}/`;

    // Si el tipo es nacionalidades, agregar el top_n
    if (tipo === "nacionalidades") {
        const topN = document.getElementById("top_n").value || 7;
        url += `?top_n=${topN}`;
    }

    $.ajax({
        url: url,
        type: "GET",
        success: function(data) {
            renderChart(tipo, data);
        },
        error: function() {
            alert("Ocurrió un error al cargar los datos del reporte.");
        }
    });
};



let chartInstance = null;

function renderChart(tipo, data) {
    const ctx = document.getElementById("grafico").getContext("2d");
    if (chartInstance) chartInstance.destroy();

    let config = {};

    if (tipo === "edad_equipo") {
        config = {
            type: 'bar',
            data: {
                labels: data.equipos,
                datasets: [{
                    label: 'Edad Promedio',
                    data: data.edades,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            }
        };
    } else if (tipo === "nacionalidades") {
        config = {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#33cc33']
                }]
            }
        };
    } else if (tipo === "valor_liga") {
        config = {
            type: 'line',
            data: {
                labels: data.ligas,
                datasets: [{
                    label: 'Valor Promedio (€)',
                    data: data.valores,
                    borderColor: 'green',
                    fill: false
                }]
            }
        };
    } else if (tipo === "top_usuarios") {
        config = {
            type: 'bar',
            data: {
                labels: data.usuarios,
                datasets: [{
                    label: 'Solicitudes',
                    data: data.solicitudes,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)'
                }]
            }
        };
    }

    chartInstance = new Chart(ctx, config);
}
