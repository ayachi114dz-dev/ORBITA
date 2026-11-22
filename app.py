
import streamlit as st
import streamlit.components.v1 as components
import math
import os
import base64

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="ORBITA | Satellite Orbit Explorer",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# PHYSICS CONSTANTS — SI UNITS
# ==================================================

EARTH_RADIUS = 6_371_000.0
MU = 3.986004418e14

# ==================================================
# FILE PATHS
# ==================================================

EARTH_PATH = os.path.join("assets", "earth.png")
SATELLITE_PATH = os.path.join("models", "satellite.glb")

# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background: radial-gradient(circle at 50% 0%, #10243c 0%, #070d18 42%, #03060c 100%);
    color: #eaf4ff;
    font-family: 'Inter', sans-serif;
}

header {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: #080f1b;
    border-right: 1px solid #18334d;
}

[data-testid="stSidebar"] * {
    color: #dcecff;
}

.hero {
    text-align: center;
    padding: 30px 10px 20px;
}

.eyebrow {
    color: #49baff;
    font-size: 12px;
    letter-spacing: 5px;
    font-weight: 600;
    margin-bottom: 12px;
}

.orbita-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 65px;
    font-weight: 800;
    letter-spacing: 10px;
    color: #f4faff;
    text-shadow: 0 0 25px rgba(40, 160, 255, 0.55);
}

.hero h3 {
    color: #8bcfff;
    font-weight: 400;
    letter-spacing: 2px;
    margin-top: 5px;
}

.hero p {
    color: #91a9c0;
    font-size: 14px;
    margin-top: 15px;
}

.section-title {
    color: #75caff;
    font-family: 'Orbitron', sans-serif;
    font-size: 17px;
    letter-spacing: 2px;
    margin: 20px 0;
}

.info-card {
    background: linear-gradient(145deg, #101f31, #091321);
    border: 1px solid #1d4261;
    border-radius: 12px;
    padding: 20px;
    min-height: 115px;
    box-shadow: 0 0 18px rgba(0, 115, 200, 0.08);
}

.info-label {
    color: #8ba9c4;
    font-size: 12px;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.info-value {
    color: #ffffff;
    font-family: 'Orbitron', sans-serif;
    font-size: 23px;
    font-weight: 600;
}

.info-unit {
    color: #5dbbff;
    font-size: 12px;
    margin-top: 5px;
}

.orbit-card {
    background: linear-gradient(145deg, #10243a, #091321);
    border: 1px solid #38a9e8;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    text-align: center;
    box-shadow: 0 0 20px rgba(49, 186, 255, 0.12);
}

.orbit-label {
    color: #8ba9c4;
    font-size: 12px;
    letter-spacing: 3px;
    margin-bottom: 10px;
}

.orbit-value {
    color: #65c7ff;
    font-family: 'Orbitron', sans-serif;
    font-size: 21px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #526d87;
    font-size: 11px;
    letter-spacing: 2px;
    padding: 30px 0 10px;
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #38bdf8 !important;
    border: 2px solid #38bdf8 !important;
}

.stButton button {
    background: #123858;
    color: white;
    border: 1px solid #318bc5;
    border-radius: 8px;
}

.stButton button:hover {
    background: #1b527d;
    border-color: #70caff;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown("""
<div style="text-align:center; padding:20px 0;">
    <div style="font-family:Orbitron; font-size:25px;
                letter-spacing:5px; color:#72caff;">
        🛰️ ORBITA
    </div>
    <div style="color:#7895ad; font-size:10px;
                letter-spacing:3px; margin-top:5px;">
        SPACE TECHNOLOGY
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Mission Overview", "Orbit Calculator"]
)

st.sidebar.markdown("---")
st.sidebar.caption("ORBITA PROJECT")
st.sidebar.caption("Exploring space through physics.")

# ==================================================
# MAIN HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">EXPLORE BEYOND THE HORIZON</div>
    <div class="orbita-title">🛰️ ORBITA</div>
    <h3>Satellite Orbit Explorer</h3>
    <p>
        Explore artificial satellites, understand orbital motion,
        and discover the physics behind space technology.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==================================================
# ORBIT CLASSIFICATION
# ==================================================

def classify_orbit(altitude_km):

    if altitude_km <= 2000:
        return "LEO — LOW EARTH ORBIT"

    elif altitude_km < 35686:
        return "MEO — MEDIUM EARTH ORBIT"

    elif altitude_km <= 35886:
        return "GEO — GEOSTATIONARY ORBIT REGION"

    else:
        return "ABOVE GEO — HIGH EARTH ORBIT"


# ==================================================
# ORBIT CALCULATIONS
# ==================================================

def calculate_orbit(altitude_km):

    altitude_m = altitude_km * 1000

    orbital_radius = EARTH_RADIUS + altitude_m

    velocity = math.sqrt(MU / orbital_radius)

    period_seconds = (
        2 * math.pi *
        math.sqrt(orbital_radius ** 3 / MU)
    )

    return orbital_radius, velocity, period_seconds


# ==================================================
# 3D EARTH AND REAL SATELLITE SCENE
# ==================================================


def create_3d_scene(altitude_km):

    if os.path.exists(EARTH_PATH):
        with open(EARTH_PATH, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        earth_texture = "data:image/png;base64," + image_data
    else:
        earth_texture = ""

    if os.path.exists(SATELLITE_PATH):
        with open(SATELLITE_PATH, "rb") as f:
            satellite_data = base64.b64encode(f.read()).decode("utf-8")
    else:
        satellite_data = ""
        st.error("Satellite model not found in models/satellite.glb")

    visual_radius = 1.45 + 1.45 * (
        min(altitude_km, 40000) / 40000
    ) ** 0.45

    html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
html, body {
    margin:0;
    padding:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:transparent;
    font-family:Arial,sans-serif;
}
#scene {
    width:100%;
    height:680px;
    position:relative;
}
#instructions {
    position:absolute;
    top:14px;
    width:100%;
    text-align:center;
    color:#9bcdf0;
    font-size:12px;
    letter-spacing:1px;
    pointer-events:none;
    z-index:5;
}
#status {
    position:absolute;
    bottom:12px;
    width:100%;
    text-align:center;
    color:#76caff;
    font-size:12px;
    letter-spacing:2px;
    pointer-events:none;
    z-index:5;
}
#hud {
    position:absolute;
    bottom:12px;
    left:18px;
    color:#9bc5e3;
    font-size:11px;
    pointer-events:none;
    z-index:5;
}
canvas {
    display:block;
}
</style>
</head>
<body>

<div id="scene">
    <div id="instructions">
        LEFT CLICK EARTH TO START / PAUSE
        &nbsp; | &nbsp; RIGHT CLICK + DRAG TO ZOOM
    </div>
    <div id="hud">ALTITUDE: __ALTITUDE_KM__ km</div>
    <div id="status">ORBIT SIMULATION: RUNNING</div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>

<script>

const container = document.getElementById("scene");
const statusText = document.getElementById("status");

const orbitRadius = __ORBIT_RADIUS__;

let running = true;
let zoom = 1;

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    38,
    container.clientWidth / container.clientHeight,
    0.1,
    300
);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    alpha:true
});

renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(container.clientWidth,container.clientHeight);
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

// LIGHTING

scene.add(new THREE.AmbientLight(0xffffff,0.65));

const sunlight = new THREE.DirectionalLight(0xfff4df,2.2);
sunlight.position.set(6,4,5);
scene.add(sunlight);

const blueLight = new THREE.DirectionalLight(0x448bff,0.7);
blueLight.position.set(-5,-2,-5);
scene.add(blueLight);

// STARS

const starPositions = [];

for(let i=0;i<2200;i++){
    const r = 75 + Math.random()*35;
    const theta = Math.random()*Math.PI*2;
    const phi = Math.acos(2*Math.random()-1);

    starPositions.push(
        r*Math.sin(phi)*Math.cos(theta),
        r*Math.cos(phi),
        r*Math.sin(phi)*Math.sin(theta)
    );
}

const starGeometry = new THREE.BufferGeometry();
starGeometry.setAttribute(
    "position",
    new THREE.Float32BufferAttribute(starPositions,3)
);

const stars = new THREE.Points(
    starGeometry,
    new THREE.PointsMaterial({
        color:0xffffff,
        size:0.28,
        transparent:true,
        opacity:0.85
    })
);

scene.add(stars);

// EARTH

const earthGroup = new THREE.Group();
earthGroup.rotation.z = THREE.MathUtils.degToRad(23.4);
scene.add(earthGroup);

const earthMaterial = new THREE.MeshPhongMaterial({
    color:0xffffff,
    shininess:22,
    specular:0x334466
});

const earth = new THREE.Mesh(
    new THREE.SphereGeometry(1,160,160),
    earthMaterial
);

earthGroup.add(earth);

// EARTH TEXTURE

const earthTexturePath = "__EARTH_TEXTURE__";

if(earthTexturePath.length > 0){

    new THREE.TextureLoader().load(
        earthTexturePath,
        function(texture){
            texture.encoding = THREE.sRGBEncoding;
            texture.anisotropy =
                renderer.capabilities.getMaxAnisotropy();

            earth.material.map = texture;
            earth.material.needsUpdate = true;
        },
        undefined,
        function(){
            console.error("Earth texture loading failed");
        }
    );

}else{
    earth.material.color.set(0x087bc1);
}

// ATMOSPHERE

const atmosphere = new THREE.Mesh(
    new THREE.SphereGeometry(1.075,128,128),
    new THREE.MeshBasicMaterial({
        color:0x279bff,
        transparent:true,
        opacity:0.13,
        side:THREE.BackSide,
        blending:THREE.AdditiveBlending,
        depthWrite:false
    })
);

earthGroup.add(atmosphere);

// OUTER ATMOSPHERE

const outerAtmosphere = new THREE.Mesh(
    new THREE.SphereGeometry(1.12,96,96),
    new THREE.MeshBasicMaterial({
        color:0x267cff,
        transparent:true,
        opacity:0.07,
        side:THREE.BackSide,
        blending:THREE.AdditiveBlending,
        depthWrite:false
    })
);

earthGroup.add(outerAtmosphere);

// ORBIT PLANE

const orbitGroup = new THREE.Group();

orbitGroup.rotation.set(
    THREE.MathUtils.degToRad(22),
    0,
    THREE.MathUtils.degToRad(-28)
);

scene.add(orbitGroup);

// ORBIT LINE

const orbitPoints = [];

for(let i=0;i<=900;i++){

    const angle = i/900*Math.PI*2;

    orbitPoints.push(
        new THREE.Vector3(
            orbitRadius*Math.cos(angle),
            0,
            orbitRadius*Math.sin(angle)
        )
    );
}

const orbitLine = new THREE.LineLoop(
    new THREE.BufferGeometry().setFromPoints(orbitPoints),
    new THREE.LineBasicMaterial({
        color:0x48bfff,
        transparent:true,
        opacity:0.9
    })
);

orbitGroup.add(orbitLine);

// SATELLITE

const satellite = new THREE.Group();
orbitGroup.add(satellite);

let satelliteLoaded = false;
const satelliteData = "__SATELLITE_MODEL__";

if(satelliteData.length > 0){

    function decodeModel(data){

        const binary = atob(data);
        const bytes = new Uint8Array(binary.length);

        for(let i=0;i<binary.length;i++){
            bytes[i] = binary.charCodeAt(i);
        }

        return bytes.buffer;
    }

    new THREE.GLTFLoader().parse(
        decodeModel(satelliteData),
        "",
        function(gltf){

            const model = gltf.scene;

            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());

            model.position.sub(center);

            const longestDimension = Math.max(
                size.x,size.y,size.z
            );

            const pivot = new THREE.Group();
            pivot.add(model);

            // Visual enlargement, not real physical scale.
            pivot.scale.setScalar(
                0.12 / Math.max(longestDimension,0.0001)
            );

            satellite.add(pivot);

            satelliteLoaded = true;
            statusText.textContent = "ORBIT SIMULATION: RUNNING";
        },
        function(error){
            console.error(error);
            statusText.textContent = "SATELLITE MODEL ERROR";
        }
    );

}else{
    statusText.textContent = "SATELLITE MODEL NOT FOUND";
}

// CAMERA

function frameCamera(){

    const width = Math.max(container.clientWidth,1);
    const height = Math.max(container.clientHeight,1);

    camera.aspect = width/height;

    const angle = THREE.MathUtils.degToRad(camera.fov/2);

    const horizontalFit =
        (orbitRadius+0.25) /
        (Math.tan(angle)*camera.aspect);

    const verticalFit = (orbitRadius+0.25)*1.35;

    const distance = Math.max(
        4.0,
        horizontalFit,
        verticalFit
    )*zoom;

    camera.position.set(
        0,
        distance*0.12,
        distance
    );

    camera.lookAt(0,0,0);
    camera.updateProjectionMatrix();
}

frameCamera();

// SATELLITE MOTION

let orbitalAngle = Math.PI/4;

function updateSatellite(){

    satellite.position.set(
        orbitRadius*Math.cos(orbitalAngle),
        0,
        orbitRadius*Math.sin(orbitalAngle)
    );

    satellite.up.set(0,1,0);
    satellite.lookAt(0,0,0);
}

// CLICK TO PAUSE

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

renderer.domElement.addEventListener("click",function(event){

    if(event.button!==0) return;

    const rect = renderer.domElement.getBoundingClientRect();

    mouse.x = ((event.clientX-rect.left)/rect.width)*2-1;
    mouse.y = -((event.clientY-rect.top)/rect.height)*2+1;

    raycaster.setFromCamera(mouse,camera);

    if(raycaster.intersectObject(earth).length>0){

        running = !running;

        statusText.textContent = running
            ? "ORBIT SIMULATION: RUNNING"
            : "ORBIT SIMULATION: PAUSED";
    }
});

// ZOOM

let dragging = false;
let previousY = 0;

renderer.domElement.addEventListener(
    "contextmenu",
    event=>event.preventDefault()
);

renderer.domElement.addEventListener("pointerdown",function(event){

    if(event.button===2){
        dragging = true;
        previousY = event.clientY;
        renderer.domElement.setPointerCapture(event.pointerId);
    }
});

renderer.domElement.addEventListener("pointerup",function(){
    dragging = false;
});

renderer.domElement.addEventListener("pointermove",function(event){

    if(dragging){

        zoom += (event.clientY-previousY)*0.004;
        zoom = Math.max(0.55,Math.min(2.2,zoom));

        previousY = event.clientY;
        frameCamera();
    }
});

// ANIMATION

function animate(){

    requestAnimationFrame(animate);

    if(running && satelliteLoaded){
        orbitalAngle += 0.008;
    }

    earth.rotation.y += 0.0007;

    updateSatellite();

    renderer.render(scene,camera);
}

updateSatellite();
animate();

// RESIZE

window.addEventListener("resize",function(){

    renderer.setSize(
        container.clientWidth,
        container.clientHeight
    );

    frameCamera();
});

</script>
</body>
</html>
"""

    html = html.replace("__EARTH_TEXTURE__", earth_texture)
    html = html.replace("__SATELLITE_MODEL__", satellite_data)
    html = html.replace("__ORBIT_RADIUS__", str(visual_radius))
    html = html.replace("__ALTITUDE_KM__", f"{altitude_km:,}")

    components.html(
        html,
        height=690,
        scrolling=False
    )

# ==================================================
# PAGE 1 — MISSION OVERVIEW
# ==================================================

if page == "Mission Overview":

    st.markdown(
        '<div class="section-title">MISSION OVERVIEW</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1, 2])

    with left:

        altitude = st.slider(
            "SELECT SATELLITE ALTITUDE",
            min_value=200,
            max_value=40000,
            value=400,
            step=50,
            format="%d km"
        )

    radius, velocity, period = calculate_orbit(altitude)

    orbit_type = classify_orbit(altitude)

    st.markdown("### ORBITAL PARAMETERS")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">ORBITAL RADIUS</div>
            <div class="info-value">{radius:,.0f}</div>
            <div class="info-unit">METERS (m)</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">ORBITAL VELOCITY</div>
            <div class="info-value">{velocity:,.2f}</div>
            <div class="info-unit">METERS / SECOND (m/s)</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">ORBITAL PERIOD</div>
            <div class="info-value">{period:,.0f}</div>
            <div class="info-unit">SECONDS (s)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ORBIT CLASSIFICATION")

    st.markdown(f"""
    <div class="orbit-card">
        <div class="orbit-label">CURRENT ORBIT TYPE</div>
        <div class="orbit-value">{orbit_type}</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        f"Selected altitude: {altitude:,} km "
        f"({altitude * 1000:,} m)"
    )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">3D EARTH ORBIT SIMULATION</div>',
        unsafe_allow_html=True
    )

    create_3d_scene(altitude)

    st.caption(
        "Left-click directly on Earth to start or pause the satellite. "
        "Right-click and drag vertically to zoom."
    )

    st.info(
        "The 3D scene is an illustrative orbital visualization. "
        "The satellite animation speed is accelerated and is not real-time."
    )


# ==================================================
# PAGE 2 — ORBIT CALCULATOR
# ==================================================

elif page == "Orbit Calculator":

    st.markdown(
        '<div class="section-title">ORBIT CALCULATOR</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Calculate the main orbital parameters "
        "of a satellite around Earth."
    )

    altitude = st.number_input(
        "Satellite altitude above Earth (km)",
        min_value=100.0,
        max_value=50000.0,
        value=400.0,
        step=50.0
    )

    radius, velocity, period = calculate_orbit(altitude)

    orbit_type = classify_orbit(altitude)

    st.markdown("---")

    st.markdown("### CALCULATION RESULTS")

    col1, col2, col3 = st.columns(3)

    col1.metric("Orbital Radius", f"{radius:,.0f} m")

    col2.metric("Orbital Velocity", f"{velocity:,.2f} m/s")

    col3.metric("Orbital Period", f"{period:,.0f} s")

    st.markdown("### ORBIT CLASSIFICATION")

    st.markdown(f"""
    <div class="orbit-card">
        <div class="orbit-label">CURRENT ORBIT TYPE</div>
        <div class="orbit-value">{orbit_type}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### PHYSICAL EQUATIONS")

    st.latex(r"r = R_E + h")

    st.latex(r"v = \sqrt{\frac{\mu}{r}}")

    st.latex(r"T = 2\pi\sqrt{\frac{r^3}{\mu}}")

    st.markdown("### CONSTANTS")

    st.write(f"Earth radius: {EARTH_RADIUS:,.0f} m")

    st.write(f"Earth gravitational parameter: {MU:.6e} m³/s²")

    st.caption(
        "All calculations use SI units and assume a circular "
        "orbit around a spherical Earth."
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    ORBITA — EXPLORING SPACE THROUGH PHYSICS AND TECHNOLOGY
</div>
""", unsafe_allow_html=True)
