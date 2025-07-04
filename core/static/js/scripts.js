function verEquipos(liga) {
    console.log("Éxito");
    const equiposPorLiga = {
        premier: {
        nombre: "Premier League",
        equipos: [
            { nombre: "Manchester City", img: "static/img/Ligas/PremierLeague/ManchesterCity/manchester-city.png" },
            { nombre: "Manchester United", img: "static/img/Ligas/PremierLeague/ManchesterUnited/manchester-united.png" },
            { nombre: "Liverpool", img: "static/img/Ligas/PremierLeague/Liverpool/liverpool.png" },
            { nombre: "Arsenal", img: "static/img/Ligas/PremierLeague/Arsenal/arsenal.png" },
            { nombre: "Chelsea", img: "static/img/Ligas/PremierLeague/Chelsea/chelsea.png" },
            { nombre: "Tottenham", img: "static/img/Ligas/PremierLeague/Tottenham/tottenham.png" },
        ]
        },
        laliga: {
        nombre: "La Liga",
        equipos: [
            { nombre: "Real Madrid", img: "static/img/Ligas/LaLiga/RealMadrid/real-madrid.png" },
            { nombre: "Barcelona", img: "static/img/Ligas/LaLiga/Barcelona/barcelona.png" },
            { nombre: "Atlético de Madrid", img: "static/img/Ligas/LaLiga/AtleticoMadrid/atletico-madrid.png" },
            { nombre: "Sevilla", img: "static/img/Ligas/LaLiga/Sevilla/sevilla.png" },
            { nombre: "Athletic Club", img: "static/img/Ligas/LaLiga/AthleticBilbao/athletic-bilbao.png" },
            { nombre: "Villarreal", img: "static/img/Ligas/LaLiga/Villarreal/villarreal.png" },
        ]
        },
        bundesliga: {
        nombre: "Bundesliga",
        equipos: [
            { nombre: "Bayern Múnich", img: "static/img/Ligas/Bundesliga/BayernMunich/bayern-munich.png" },
            { nombre: "Borussia Dortmund", img: "static/img/Ligas/Bundesliga/BorussiaDortmund/borussia-dortmund.png" },
            { nombre: "RB Leipzig", img: "static/img/Ligas/Bundesliga/Leipzig/rb-leipzig.png" },
            { nombre: "Bayer Leverkusen", img: "static/img/Ligas/Bundesliga/BayerLeverkusen/bayer-leverkusen.png" },
            { nombre: "Eintracht Frankfurt", img: "static/img/Ligas/Bundesliga/EintrachtFrankfurt/eintracht-frankfurt.png" },
            { nombre: "Wolfsburgo", img: "static/img/Ligas/Bundesliga/Wolfsburgo/wolfsburgo.png" },
        ]
        },
        seriea: {
        nombre: "Serie A",
        equipos: [
            { nombre: "Juventus", img: "static/img/Ligas/SerieA/Juventus/juventus.png" },
            { nombre: "AC Milan", img: "static/img/Ligas/SerieA/AcMilan/ac-milan.png" },
            { nombre: "Inter de Milan", img: "static/img/Ligas/SerieA/InterMilan/inter-milan.png" },
            { nombre: "Napoli", img: "static/img/Ligas/SerieA/Napoli/napoli.png" },
            { nombre: "Roma", img: "static/img/Ligas/SerieA/Roma/roma.png" },
            { nombre: "Lazio", img: "static/img/Ligas/SerieA/Lazio/lazio.png" },
        ]
        },
        ligue1: {
        nombre: "Ligue 1",
        equipos: [
            { nombre: "PSG", img: "static/img/Ligas/Ligue1/PSG/psg.png" },
            { nombre: "Olympique Lyon", img: "static/img/Ligas/Ligue1/OlympiqueLyon/olympique-lyon.png" },
            { nombre: "Olympique Marsella", img: "static/img/Ligas/Ligue1/OlympiqueMarsella/olympique-marsella.png" },
            { nombre: "Lille", img: "static/img/Ligas/Ligue1/Lille/lille.png" },
            { nombre: "Monaco", img: "static/img/Ligas/Ligue1/ASMonaco/monaco.png" },
            { nombre: "Stade Rennes", img: "static/img/Ligas/Ligue1/Rennes/rennes.png" },
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
            <img src="${equipo.img}" alt="${equipo.nombre}" class="img-fluid rounded shadow-sm equipo-img" 
                style="max-height: 100px; cursor: pointer;" 
                onclick="verJugadores('${liga}', '${equipo.nombre}')">
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

function verJugadores(liga, equipo) {
  const jugadoresPorEquipo = {
    "Manchester City": [
      { nombre: "Erling Haaland", edad: 23, img: "static/img/Jugadores/Haaland.png" },
      { nombre: "Kevin De Bruyne", edad: 32, img: "static/img/Jugadores/DeBruyne.png" }
    ],
    "Real Madrid": [
      { nombre: "Jude Bellingham", edad: 20, img: "static/img/Jugadores/Bellingham.png" },
      { nombre: "Vinícius Jr", edad: 23, img: "static/img/Jugadores/Vinicius.png" }
    ],
    // Agrega los demás equipos aquí
  };

  const jugadores = jugadoresPorEquipo[equipo];
  const contenedor = document.getElementById('contenedor-jugadores');
  contenedor.innerHTML = ""; // Limpiar

  if (jugadores && jugadores.length > 0) {
    jugadores.forEach(jugador => {
      const item = document.createElement('div');
      item.className = 'list-group-item d-flex align-items-center';

      item.innerHTML = `
        <img src="${jugador.img}" alt="${jugador.nombre}" class="rounded me-3" style="width: 50px; height: 50px;">
        <div>
          <strong>${jugador.nombre}</strong><br>
          <small>Edad: ${jugador.edad}</small>
        </div>
      `;

      contenedor.appendChild(item);
    });

    document.getElementById('jugadoresModalLabel').textContent = `Jugadores de ${equipo}`;

    const jugadoresModal = new bootstrap.Modal(document.getElementById('jugadoresModal'));
    jugadoresModal.show();
  } else {
    alert(`No se encontraron jugadores para ${equipo}`);
  }
}

function ocultar(){
    $("#PaginaM").innerHTML("");
}
