import asyncio
import os

import httpx
import streamlit as st
import streamlit.components.v1 as components
from st_keyup import st_keyup
from streamlit_javascript import st_javascript

global_client_ip = None
global_geo = { "latitude": 6.2529, "longitude": -75.5646 }
global_select = { "department_select": "Selecciona el departamento", "city_select": "Selecciona la ciudad" }
global_address = ""
global_address_select = ""
global_address_select_last = ""
global_complement_place = ""
global_data = None

global_colombia = {
    "Selecciona el departamento": [],
    "Amazonas": ["Leticia", "Puerto Nariño"],
    "Antioquia": ["Medellín", "Bello", "Itagüí", "Envigado", "Turbo", "Rionegro", "Apartadó", "Sabanalarga", "Caucasia", "Caldas", "Chigorodó", "Sabaneta", "Copacabana", "La Estrella", "Necoclí", "La Ceja", "Marinilla", "Carmen de Viboral", "Barbosa", "El Bagre", "Girardota", "Guarne", "Carepa", "Urrao", "Arboletes", "Andes", "Cáceres", "Yarumal", "Segovia", "Puerto Berrío", "Tarazá", "Santa Rosa de Osos", "Sonsón", "Santuario", "Yarumal", "San Pedro de Urabá", "Remedios", "Amagá", "Ciudad Bolívar", "San Juan de Urabá", "Nechí", "Yolombó", "Valdivia", "Donmatías", "Zaragoza", "Ituango", "Dabeiba", "Amalfi", "Santa Fe de Antioquia", "Mutatá", "Puerto Triunfo", "Santa Bárbara", "Fredonia", "Abejorral", "Concordia", "Frontino", "La Unión", "San Vicente", "Salgar", "Yondó", "Betulia", "Retiro", "San Roque", "Anorí", "San Jerónimo", "Támesis", "Cocorná", "San Carlos", "Sopetrán", "Titiribí", "Jardín", "Cañasgordas", "San Rafael", "Puerto Nare", "Ebéjico", "Jericó", "Cisneros", "Valdivia", "Santo Domingo", "Angostura", "Venecia", "Granada", "Vegachí", "Betania", "Guatapé", "Campamento", "Angelópolis", "Argelia", "Entrerríos", "Briceño", "Pueblorrico", "Nariño", "Yalí"],
    "Arauca": ["Arauca", "Saravena", "Tame", "Arauquita", "Fortul"],
    "Atlántico": ["Barranquilla", "Soledad", "Malambo", "Sabanalarga", "Galapa", "Baranoa", "Puerto Colombia", "Sabanagrande", "Santo Tomás", "Palmar de Varela", "Luruaco", "Repelón", "Polonuevo", "Ponedera", "Campo de la Cruz", "Juan de Acosta", "Usiacurí", "Manatí", "Candelaria", "Santa Lucía", "Tubará", "Suan"],
    "Bolívar": ["Cartagena", "Magangué", "Turbaco", "Arjona", "Turbaná", "El Carmen de Bolívar", "María la Baja", "Santa Rosa del Sur", "San Pablo", "San Juan Nepomuceno", "Mahates", "Pinillos", "Morales", "Santa Rosa", "Calamar", "Achí", "Tiquisio", "San Jacinto", "Montecristo", "Villanueva", "Simití", "San Estanislao", "San Martín de Loba", "Barranco de Loba", "Santa Catalina", "Clemencia", "Altos del Rosario", "San Jacinto del Cauca", "Cicuco", "Hatillo de Loba", "Córdoba", "Zambrano", "Talaigua Nuevo", "Regidor", "Arroyohondo", "Margarita", "Norosí", "San Fernando", "San Fernando"],
    "Boyacá": ["Tunja", "Duitama", "Sogamoso", "Chiquinquirá", "Puerto Boyacá", "Paipa", "Villa de Leyva", "Moniquirá", "Samacá", "Garagoa", "Nobsa", "Aquitania", "Ventaquemada", "Cómbita", "Tibasosa", "Ráquira", "Saboyá", "Santa Rosa de Viterbo", "Úmbita", "Toca", "Ramiriquí", "Socotá", "Tuta", "Guateque", "Chita", "Pesca", "Tibaná", "Siachoque", "Muzo"],
    "Caldas": ["Manizales", "La Dorada", "Riosucio", "Villamaría", "Chinchiná", "Anserma", "Neira", "Supía", "Pensilvania", "Samaná", "Manzanares", "Aguadas", "Salamina", "Palestina", "Pácora", "Viterbo", "Marquetalia", "Aranzazu", "Belalcázar", "Filadelfia", "Risaralda"],
    "Caquetá": ["Florencia", "San Vicente del Caguán", "Cartagena del Chairá", "Puerto Rico", "Solano", "El Doncello", "El Paujíl", "La Montañita", "San José del Fragua", "Belén de los Andaquíes", "Solita"],
    "Casanare": ["Yopal", "Aguazul", "Tauramena", "Paz de Ariporo", "Villanueva", "Monterrey", "Maní", "Trinidad", "Nunchía", "Orocué"],
    "Cauca": ["Popayán", "Santander de Quilichao", "El Tambo", "La Vega", "Puerto Tejada", "Bolívar", "Miranda", "Cajibío", "Patía", "El Bordo", "Belalcázar", "Piendamó", "Buenos Aires", "Caldono", "Timbío", "Corinto", "Silvia", "Inzá", "Guapí", "Argelia", "Morales", "Toribío", "Balboa", "Caloto", "Timbiquí", "Almaguer", "Suárez", "Villa Rica", "Totoró", "Jambaló", "Coconuco", "Mercaderes", "Villa Rica", "Rosas", "Paispamba", "Padilla", "La Sierra", "San Sebastián", "Piamonte", "Sucre"],
    "Cesar": ["Valledupar", "Aguachica", "Agustín Codazzi", "La Jagua de Ibirico", "Bosconia", "Chimichagua", "El Copey", "Pueblo Bello", "Chiriguaná", "San Alberto", "El Paso", "Curumaní", "Pailitas", "Becerril", "San Martín", "San Diego", "Astrea", "Pelaya", "La Gloria", "Río de Oro", "Tamalameque", "Gamarra", "González"],
    "Chocó": ["Quibdó", "Riosucio", "Pie de Pató", "Istmina", "Tadó", "Pizarro", "Condoto", "El Carmen de Atrato", "Bagadó", "Unguía", "Acandí", "Santa Genoveva de Docordó", "Lloró", "Bellavista", "Mutis", "Nuquí", "Juradó"],
    "Córdoba": ["Montería", "Cereté", "Sahagún", "Montelíbano", "Tierralta", "Planeta Rica", "Ciénaga de Oro", "Puerto Libertador", "Lorica", "Chinú", "San Andrés de Sotavento", "Ayapel", "Valencia", "San Pelayo", "Pueblo Nuevo", "Tuchín", "San Bernardo del Viento", "San Antero", "Puerto Escondido", "Moñitos", "San Carlos", "Los Córdobas", "Canalete", "Buenavista", "Buenavista", "Momil", "Cotorra", "La Apartada", "Purísima de la Concepción", "Chimá"],
    "Cundinamarca": ["Bogotá", "Fontibón", "Usme", "Soacha", "Zipaquirá", "Fusagasugá", "Facatativá", "Girardot", "Mosquera", "Chía", "Madrid", "Funza", "Cajicá", "Villeta", "Guaduas", "Villa de San Diego de Ubaté", "Sibaté", "Tocancipá", "La Mesa", "Cota", "Tabio", "Sopó", "La Calera", "Pacho", "Chocontá", "Cogua", "El Colegio", "Silvania", "Villapinzón", "Tenjo", "El Rosal", "Tocaima", "Suesca", "Cáqueza", "Gachancipá", "Subachoque", "Guasca", "Puerto Salgar", "Anapoima", "Sesquilé", "Nemocón", "Agua de Dios", "La Vega", "San Antonio del Tequendama", "Simijaca", "Anolaima", "Ricaurte", "Viotá", "Susa", "Arbeláez", "Fómeque", "Pasca", "Guachetá", "Gachetá", "La Palma", "Yacopí", "Choachí", "Ubalá", "Caparrapí", "Lenguazaque", "Medina", "Cachipay", "Sasaima", "Bojacá", "Granada", "Une", "Carmen de Carupa", "Tena", "Tausa", "Junín"],
    "Guainía": ["Inírida"],
    "Guaviare": ["San José del Guaviare", "El Retorno", "Calamar"],
    "Huila": ["Palermo", "Neiva", "Pitalito", "Garzón", "La Plata", "Acevedo", "Gigante", "Campoalegre", "San Agustín", "Aipe", "Isnos", "Algeciras", "Rivera", "Guadalupe", "Suaza", "Timaná", "Tarqui", "La Argentina", "Pital", "Oporapa", "Palestina", "Tello", "Santa María", "Saladoblanco", "Tesalia", "Íquira", "Yaguará", "Teruel"],
    "La Guajira": ["Uripa", "Ríohacha", "Maicao", "Uribia", "Manaure", "Fonseca", "San Juan del Cesar", "Dibulla", "Barrancas", "Villanueva", "Hatonuevo", "Urumita", "Albania", "Distracción", "El Molino"],
    "Magdalena": ["Santa Marta", "Ciénaga", "Fundación", "El Banco", "Plato", "Aracataca", "Pivijay", "Puebloviejo", "El Difícil", "Sitionuevo", "Guamal", "Santa Ana", "Chivolo", "Nueva Granada", "El Retén", "San Sebastián de Buenavista", "Tíogollo", "El Piñón", "Pijiño del Carmen", "Tenerife", "Algarrobo", "Algarrobo", "Santa Bárbara de Pinto", "San Antonio", "Concordia", "San Zenón", "Buenavista"],
    "Meta": ["Villavicencio", "Acacías", "Granada", "Puerto Gaitán", "La Macarena", "Puerto López", "San Martín", "Vistahermosa", "Puerto Concordia", "Cumaral", "Restrepo", "Guamal", "Castilla La Nueva", "Fuente de Oro", "San Carlos de Guaroa", "Puerto Rico", "Hato Corozal", "Lejanías", "Mesetas", "Puerto Lleras", "San Juan de Arama"],
    "Nariño": ["Pasto", "Tumaco", "Ipiales", "Samaniego", "El Charco", "Túquerres", "Cumbal", "Barbacoas", "Bocas de Satinga", "Guachavés", "Buesaco", "San José", "La Unión", "Sandoná", "San José", "Taminango", "San Bernardo", "Sotomayor", "San Lorenzo", "Guachucal", "Ricaurte", "La Cruz", "Pupiales", "El Peñol", "Córdoba", "El Tablón", "San Pablo", "Chachagüí", "El Tambo", "Guaitarilla", "Yacuanquer", "Mosquera", "Potosí", "Génova", "Consacá", "La Florida", "Iscuandé", "Linares", "Ospina", "Carlosama", "Iles"],
    "Norte de Santander": ["Cúcuta", "Ocaña", "Villa del Rosario", "Los Patios", "Pamplona", "Ábrego", "Tibú", "El Zulia", "Teorama", "Sardinata", "Convención", "Toledo", "Chinácota", "El Carmen", "La Esperanza", "Cáchira", "Tarrá", "El Tarra", "Chitagá", "Puerto Santander", "San Calixto", "Hacarí", "Arboledas"],
    "Putumayo": ["Puerto Asís", "Orito", "Mocoa", "Valle del Guamuez", "La Dorada", "Puerto Leguízamo", "Puerto Guzmán", "Villagarzón", "Puerto Guzmán", "Sibundoy", "Puerto Caicedo"],
    "Quindío": ["Armenia", "Calarcá", "La Tebaida", "Montenegro", "Quimbaya", "Circasia", "Filandia"],
    "Risaralda": ["Pereira", "Dosquebradas", "Santa Rosa de Cabal", "Quinchía", "La Virginia", "Belén de Umbría", "Marsella", "Mistrató", "Santuario", "Apía", "Guática", "Pueblo Rico", "La Celia"],
    "San Andrés y Providencia": ["San Andrés"],
    "Santander": ["Bucaramanga", "Barrancabermeja", "Floridablanca", "Girón", "Piedecuesta", "San Gil", "Cimitarra", "Lebrija", "Puerto Wilches", "Socorro", "Barbosa", "San Vicente de Chucurí", "Rionegro", "Sabana de Torres", "El Carmen de Chucurí", "Vélez", "Málaga", "Landázuri", "Los Santos", "Curití", "Oiba", "Bolívar", "Puente Nacional", "El Playón", "Mogotes", "Charalá", "Suaita", "Zapatoca", "La Belleza"],
    "Sucre": ["Sincelejo", "Corozal", "San Marcos", "San Onofre", "Sampués", "Santiago de Tolú", "San Luis de Sincé", "Majagual", "San Benito Abad", "Sucre", "Los Palmitos", "Galeras", "Ovejas", "Tolú Viejo", "San Pedro", "Guaranda", "Morroa", "Palmito", "San Juan de Betulia", "Caimito", "La Unión", "Coveñas", "Buenavista", "El Roble"],
    "Tolima": ["Ibagué", "Espinal", "Chaparral", "Líbano", "Melgar", "San Sebastián de Mariquita", "Ortega", "Guamo", "Planadas", "Fresno", "Purificación", "Flandes", "Coyaima", "Rioblanco", "Honda", "Natagaima", "Rovira", "Venadillo", "Anzoátegui", "Cajamarca", "Lérida", "San Antonio", "Saldaña", "Ataco", "Guayabal", "Icononzo", "Villahermosa", "Coello", "Cunday", "Falan", "Palocabildo", "Carmen de Apicalá", "Alvarado"],
    "Valle del Cauca": ["Cali", "Buenaventura", "Palmira", "Tuluá", "Cartago", "Jamundí", "Guadalajara de Buga", "Candelaria", "Yumbo", "Florida", "Pradera", "El Cerrito", "Zarzal", "Sevilla", "La Unión", "Dagua", "Guacarí", "Roldanillo", "Caicedonia", "Andalucía", "Ginebra", "Bugalagrande", "Ansermanuevo", "Trujillo", "San Pedro", "Toro", "Yotoco", "Restrepo", "Darién", "Obando", "Riofrío", "Bolívar", "La Victoria", "Alcalá", "La Cumbre", "El Águila", "Vijes", "El Cairo", "El Dovio"],
    "Vaupés": ["Mitú"],
    "Vichada": ["Cumaribo", "La Primavera", "Puerto Carreño"]
}

async def get_geo_service(client_ip: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://tools.keycdn.com/geo?host={client_ip}", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}, timeout=None)
        html = response.text
        html_geo_plots = html[html.index('geoPlots') + 10:]
        geo_plots = html_geo_plots[:html_geo_plots.index('</script>')]
        latitude = geo_plots[geo_plots.index('latitude'):].split(':')[1].split(",")[0].strip()
        longitude = geo_plots[geo_plots.index('longitude'):].split(':')[1].split(",")[0].strip()
        return { "latitude": float(latitude), "longitude": float(longitude) }

async def autocomplete(input: str, latitude: float, longitude: float):
    api_key = st.secrets["google_api_key"]
    content = {
        "input": input,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 5000.0
            }
        }
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://places.googleapis.com/v1/places:autocomplete", content=str(content), headers={"Content-Type": "application/json", "X-Goog-Api-Key": api_key}, timeout=None)
        return response.json()

async def get_geocode(place_id: str):
    api_key = st.secrets["google_api_key"]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://maps.googleapis.com/maps/api/geocode/json?place_id={place_id}&key={api_key}", timeout=None)
        return response.json()

@st.cache_resource
def get_client_ip():
    return global_client_ip

@st.cache_resource
def get_geo():
    return global_geo

@st.cache_resource
def get_address():
    return global_address

@st.cache_resource
def get_address_select():
    return global_address_select

@st.cache_resource
def get_address_select_last():
    return global_address_select_last

@st.cache_resource
def get_select():
    return global_select

@st.cache_resource
def get_complement_place():
    return global_complement_place

@st.cache_resource
def get_data():
    return global_data

def others():
    st.session_state.others = True

def wide_space_default():
    st.set_page_config(layout="wide")
    
async def main():

    wide_space_default()

    st.html("""
        <style>
            .stAppHeader {
                display: none;
            }
            div[data-testid="stMainBlockContainer"] {
                padding: 0rem 0rem 0rem 0rem;
                margin-left: auto;
                margin-right: auto;
                max-width: 75rem;
            }
            div[data-testid="stElementContainer"]:has(.stIFrame) {
                padding: 0rem 0rem 0rem 0rem;
            }
            div[data-testid="stElementContainer"]:has(iframe[height="0"]) {
                display: none;
            }
            .st-key-st_keyup_address__False__hidden__500__default__Ingresa-tu-direccion {
                z-index: 99999;
            }
            .st-key-complement {
                margin: -3.1rem 0rem 0rem 0rem;
            }
            div[data-testid="stLayoutWrapper"]:has(.st-key-place) {
                position: absolute;
                margin-top: 530px;
                z-index: 99999;
                background-color: white;
                box-shadow: 0 6px 16px 0 rgba(0, 0, 0, .1);
                width: auto;
            }
            div[data-testid="stLayoutWrapper"]:has(.st-key-place) div[data-testid="stVerticalBlock"] {
                gap: 0rem;
            }
            div[data-testid="stLayoutWrapper"]:has(.st-key-place) div[data-testid="stVerticalBlock"] button {
                border: 0px solid rgba(49, 51, 63, 0.2);
                min-width: 500px;
            }
            div[data-testid="stLayoutWrapper"]:has(.st-key-place) div[data-testid="stVerticalBlock"] div[data-testid="stElementContainer"]:last-child button {
                color: #A50034;
            }
            div[data-testid="stElementContainer"]:has(.stCode) {
                margin-top: 40px;
                border: 2px solid rgba(49, 51, 63, 0.2);
            }
            div[data-testid="stElementContainer"]:has(.stCode) pre {
                background: #8b90cb;
            }
            div[data-testid="stElementContainer"]:has(.stJson) {
                margin-top: -20px;
                border: 2px solid rgba(49, 51, 63, 0.2);
            }
            .st-key-login {
                position: absolute;
                bottom: 50%;
                right: 50%;
            }
            .st-key-logout {
                position: absolute;
                bottom: 0;
                right: 0;
            }
        </style>
    """)

    if not st.user.is_logged_in:
        st.button("Log in with Google", on_click=st.login, key="login")
        st.stop()

    components.html(
        """
        <link href="https://www.negocioleonisa.com/wps/contenthandler/!ut/p/digest!xg7HWShykXcXx8VKc_Ntzg/sp/mashup:ra:collection?soffset=0&amp;eoffset=7&amp;themeID=ZJ_9HK81282NO6N80QP3JP28731L4&amp;locale=es&amp;locale=en&amp;mime-type=text%2Fcss&amp;lm=1710604851452&amp;entry=wp_toolbar_common__0.0%3Ahead_css&amp;entry=wp_theme_portal_edit_85__0.0%3Ahead_css&amp;entry=wp_theme_portal_85__0.0%3Ahead_css&amp;entry=wp_portlet_css__0.0%3Ahead_css&amp;entry=wp_simple_contextmenu_css__0.0%3Ahead_css&amp;entry=wp_status_bar__0.0%3Ahead_css" type="text/css" rel="stylesheet">
        <link href="https://www.negocioleonisa.com/wps/contenthandler/!ut/p/digest!ZRpQXtDuQFF0lasfhL-7yg/dav/fs-type1/themes/DrizzleVotreThemePaises/css/utiles.css" rel="stylesheet" type="text/css" title="assigned">
        <link href="https://www.negocioleonisa.com/wps/contenthandler/dav/fs-type1/themes/DrizzleVotreThemePaises/css/utiles.css" rel="stylesheet">
        <link href="https://www.negocioleonisa.com/VotreTheme9/themes/html/dynamicSpots/css/toolkit.css" rel="stylesheet" type="text/css">
        <link href="https://www.negocioleonisa.com/VotreTheme9/themes/html/dynamicSpots/css/design-system-votre.min.css" rel="stylesheet">
        <body class="PageGirdle PageGirdle--simple js-PageGirdle drizzle_body toolbar-closed">
            <header class="PageGirdle-header">
                <div class="PageGirdle-headerTop ">
                    <div class="Masthead u-contain">
                        <div class="Masthead-logo" aria-label="Leonisa home">
                            <div class="icon icon-leonisa-logo"></div>
                        </div>
                    </div>
                </div>
            </header>
            <div class="PageGirdle-content">
            <div class="js-PageGirdle-scrollingFix js-Modal-scrollingFix">
                <main id="main" aria-label="Content">
                    <!-- required - do not remove -->
                    <div style="display:none" id="portletState">{}</div><div id="layoutContainers" class="wpthemeLayoutContainers wpthemeLayoutContainersHidden">
                        <div class="wpthemeInner">
                            <div class="hiddenWidgetsDiv">
    <div class="component-container rowFull hiddenWidgetsContainer row ibmDndColumn id-Z7_LIT3SLS6VF3JN76IPTIMSN4S42" name="ibmHiddenWidgets"></div><div style="clear:both"></div>
    </div>

    <div class="ibmDndColumn Grid Grid--withGap u-contain" name="rowOne">
        <div class="component-container u-lg-spaceTop4 Grid-cell u-sm-size12of12 u-lg-size12of12 ibmDndColumn id-Z7_TFSJJITP7NAMNFUC5QA4LBV5E6" name="contentApp"><div class="component-control id-Z7_9HK81282N8OQ70QD09V443B335 col-12 col-md-12 col-lg-12 col-xl-12 col-xxl-12 p-0" style="visibility: visible;"><span id="Z7_9HK81282N8OQ70QD09V443B335"></span><section class="ibmPortalControl wpthemeControl wpthemeHidden a11yRegionTarget" role="region" aria-label="titulo-autoinscripcion">

        
        <!-- start header markup -->
        <header class="wpthemeControlHeader" role="banner" aria-label="skinHeaderZ7_9HK81282N8OQ70QD09V443B335">
            <div class="wpthemeInner">
                <h2>
                    <img class="dndHandle" draggable="true" ondragstart="wpModules.dnd.util.portletDragStart(event, this, this.parentNode, 30, 0);" ondragend="wpModules.dnd.util.portletDragEnd(event);" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="">
                    <!-- lm-dynamic-title node marks location for dynamic title support -->
                    <span class="lm-dynamic-title asa.portlet.title a11yRegionLabel">titulo-autoinscripcion</span>
                </h2>
                <a aria-haspopup="true" aria-label="Mostrar menú de contenido" role="button" href="javascript:;" class="wpthemeIcon wpthemeMenuFocus contextMenuInSkinIcon" style="display:none" tabindex="0">
                    <span title="Mostrar menú de contenido"><img aria-label="Mostrar menú de contenido" alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"></span>
                    <span class="wpthemeAltText">Menú de acciones de componente</span>
                    <!-- start CAM template -->
                    <span class="wpthemeMenu" data-positioning-handler="horizontallyCenteredBelow">
                        <div class="wpthemeMenuBorder">
                            <!-- define the menu item template inside the "ul" element.  only "css-class", "description", and "title" are handled by the theme's sample javascript. -->
                            <ul class="wpthemeMenuDropDown wpthemeTemplateMenu" role="menu">
                                <li class="${css-class}" role="menuitem" tabindex="-1"><span class="wpthemeMenuText">${title}</span></li>
                            </ul>
                            <div class="verticalMenuPointer pointer"></div>
                        </div> <!-- Template for loading -->
                        <div class="wpthemeMenuLoading wpthemeTemplateLoading">${loading}</div>
                        <!-- Template for submenu -->
                        <div class="wpthemeAnchorSubmenu wpthemeTemplateSubmenu">
                            <div class="wpthemeMenuBorder wpthemeMenuSubmenu">
                                <ul id="${submenu-id}" class="wpthemeMenuDropDown" role="menu">
                                    <li role="menuitem" tabindex="-1"></li>
                                </ul>
                            </div>
                        </div>
                    </span>
                    <!-- end CAM template -->
                </a>
                <a aria-haspopup="true" aria-label="Mostrar menú de portlet" role="button" href="javascript:;" class="wpthemeIcon wpthemeMenuFocus" tabindex="0" onclick="if (typeof wptheme != 'undefined') wptheme.contextMenu.init({ 'node': this, menuId: 'skinAction', jsonQuery: {'navID':ibmCfg.portalConfig.currentPageOID,'windowID':wptheme.getWindowIDFromSkin(this)}, params: {'alignment':'right'}});" onkeydown="javascript:if (typeof i$ != 'undefined' &amp;&amp; typeof wptheme != 'undefined') {if (event.keyCode ==13 || event.keyCode ==32 || event.keyCode==38 || event.keyCode ==40) {wptheme.contextMenu.init(this, 'skinAction', {'navID':ibmCfg.portalConfig.currentPageOID,'windowID':wptheme.getWindowIDFromSkin(this)}); return false;}}">
                    <span title="Mostrar menú de portlet"><img aria-label="Mostrar menú de portlet" alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"></span>
                    <span class="wpthemeAltText">Acciones</span>
                </a>
            </div>
        </header>
        
        <div class="wpthemeControlBody wpthemeOverflowAuto wpthemeClear"> <!-- lm:control dynamic spot injects markup of layout control -->
        <!-- asa.overlay marks the node that the AsaOverlayWidget will be placed in -->
            <div style="position:relative; z-index: 1;">
                <div class="analytics.overlay"></div>
            </div>

    <input type="hidden" id="titulo-autoinscripcion">
    <div class="Grid Grid--alignCenter u-sm-padTop1 u-md-padTopNone u-lg-padTopNone u-sm-padLeft1 u-sm-padRight1" dir="ltr">
    <div class="Grid-cell u-md-size12of12   u-textNormal u-textSize">
    <div class="u-textCenter u-textSize01" style="text-align: center;"><strong><span class="u-lg-textSize3  u-textSize2 u-textBold u-lineHeight">Inscríbete a nuestra </span></strong></div>

    <div class="u-textCenter u-textSize01" style="text-align: center;"><strong><span class="u-lg-textSize3  u-textSize2 u-textBold u-lineHeight">COMPRA POR CATÁLOGO</span></strong></div>

    <p class="u-textCenter u-textSize01" style="text-align: center;">&nbsp;</p>

    <div class="u-textCenter u-textSize01" style="text-align: center;">Haz parte de la marca de <strong>ROPA INTERIOR</strong> más reconocida de América Latina y ofrece más de <strong>4.000 opciones de productos</strong> de nuestro catálogo:</div>

    <div class="u-textCenter u-textSize01" style="text-align: center;">moda interior, fajas, vestidos de baño, ropa deportiva, productos complementarios y más.</div>
    </div>
    </div>
        
    <div class="wpthemeClear"></div>
        </div>
    </section>
    </div><div class="component-control id-Z7_9HK81282N8OQ70QD09V443RGM5 col-12 col-md-12 col-lg-12 col-xl-12 col-xxl-12 p-0" style="visibility: visible;"><span id="Z7_9HK81282N8OQ70QD09V443RGM5"></span><section class="ibmPortalControl wpthemeControl wpthemeHidden a11yRegionTarget" role="region" aria-label="sp-autoinscripcion-dos-pasos">

        
        <!-- start header markup -->
        <header class="wpthemeControlHeader" role="banner" aria-label="skinHeaderZ7_9HK81282N8OQ70QD09V443RGM5">
            <div class="wpthemeInner">
                <h2>
                    <img class="dndHandle" draggable="true" ondragstart="wpModules.dnd.util.portletDragStart(event, this, this.parentNode, 30, 0);" ondragend="wpModules.dnd.util.portletDragEnd(event);" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="">
                    <!-- lm-dynamic-title node marks location for dynamic title support -->
                    <span class="lm-dynamic-title asa.portlet.title a11yRegionLabel">sp-autoinscripcion-dos-pasos</span>
                </h2>
                <a aria-haspopup="true" aria-label="Mostrar menú de contenido" role="button" href="javascript:;" class="wpthemeIcon wpthemeMenuFocus contextMenuInSkinIcon" style="display:none" tabindex="0">
                    <span title="Mostrar menú de contenido"><img aria-label="Mostrar menú de contenido" alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"></span>
                    <span class="wpthemeAltText">Menú de acciones de componente</span>
                    <!-- start CAM template -->
                    <span class="wpthemeMenu" data-positioning-handler="horizontallyCenteredBelow">
                        <div class="wpthemeMenuBorder">
                            <!-- define the menu item template inside the "ul" element.  only "css-class", "description", and "title" are handled by the theme's sample javascript. -->
                            <ul class="wpthemeMenuDropDown wpthemeTemplateMenu" role="menu">
                                <li class="${css-class}" role="menuitem" tabindex="-1"><span class="wpthemeMenuText">${title}</span></li>
                            </ul>
                            <div class="verticalMenuPointer pointer"></div>
                        </div> <!-- Template for loading -->
                        <div class="wpthemeMenuLoading wpthemeTemplateLoading">${loading}</div>
                        <!-- Template for submenu -->
                        <div class="wpthemeAnchorSubmenu wpthemeTemplateSubmenu">
                            <div class="wpthemeMenuBorder wpthemeMenuSubmenu">
                                <ul id="${submenu-id}" class="wpthemeMenuDropDown" role="menu">
                                    <li role="menuitem" tabindex="-1"></li>
                                </ul>
                            </div>
                        </div>
                    </span>
                    <!-- end CAM template -->
                </a>
                <a aria-haspopup="true" aria-label="Mostrar menú de portlet" role="button" href="javascript:;" class="wpthemeIcon wpthemeMenuFocus" tabindex="0" onclick="if (typeof wptheme != 'undefined') wptheme.contextMenu.init({ 'node': this, menuId: 'skinAction', jsonQuery: {'navID':ibmCfg.portalConfig.currentPageOID,'windowID':wptheme.getWindowIDFromSkin(this)}, params: {'alignment':'right'}});" onkeydown="javascript:if (typeof i$ != 'undefined' &amp;&amp; typeof wptheme != 'undefined') {if (event.keyCode ==13 || event.keyCode ==32 || event.keyCode==38 || event.keyCode ==40) {wptheme.contextMenu.init(this, 'skinAction', {'navID':ibmCfg.portalConfig.currentPageOID,'windowID':wptheme.getWindowIDFromSkin(this)}); return false;}}">
                    <span title="Mostrar menú de portlet"><img aria-label="Mostrar menú de portlet" alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"></span>
                    <span class="wpthemeAltText">Acciones</span>
                </a>
            </div>
        </header>
        
        <div class="wpthemeControlBody wpthemeOverflowAuto wpthemeClear"> <!-- lm:control dynamic spot injects markup of layout control -->
        <!-- asa.overlay marks the node that the AsaOverlayWidget will be placed in -->
            <div style="position:relative; z-index: 1;">
                <div class="analytics.overlay"></div>
            </div>




                                <script>!function(e){var n="https://s.go-mpulse.net/boomerang/";if("False"=="True")e.BOOMR_config=e.BOOMR_config||{},e.BOOMR_config.PageParams=e.BOOMR_config.PageParams||{},e.BOOMR_config.PageParams.pci=!0,n="https://s2.go-mpulse.net/boomerang/";if(window.BOOMR_API_key="ZUQPP-8TEYN-A7YX5-VYWRZ-Z8K5D",function(){function e(){if(!o){var e=document.createElement("script");e.id="boomr-scr-as",e.src=window.BOOMR.url,e.async=!0,i.parentNode.appendChild(e),o=!0}}function t(e){o=!0;var n,t,a,r,d=document,O=window;if(window.BOOMR.snippetMethod=e?"if":"i",t=function(e,n){var t=d.createElement("script");t.id=n||"boomr-if-as",t.src=window.BOOMR.url,BOOMR_lstart=(new Date).getTime(),e=e||d.body,e.appendChild(t)},!window.addEventListener&&window.attachEvent&&navigator.userAgent.match(/MSIE [67]\./))return window.BOOMR.snippetMethod="s",void t(i.parentNode,"boomr-async");a=document.createElement("IFRAME"),a.src="about:blank",a.title="",a.role="presentation",a.loading="eager",r=(a.frameElement||a).style,r.width=0,r.height=0,r.border=0,r.display="none",i.parentNode.appendChild(a);try{O=a.contentWindow,d=O.document.open()}catch(_){n=document.domain,a.src="javascript:var d=document.open();d.domain='"+n+"';void(0);",O=a.contentWindow,d=O.document.open()}if(n)d._boomrl=function(){this.domain=n,t()},d.write("<bo"+"dy onload='document._boomrl();'>");else if(O._boomrl=function(){t()},O.addEventListener)O.addEventListener("load",O._boomrl,!1);else if(O.attachEvent)O.attachEvent("onload",O._boomrl);d.close()}function a(e){window.BOOMR_onload=e&&e.timeStamp||(new Date).getTime()}if(!window.BOOMR||!window.BOOMR.version&&!window.BOOMR.snippetExecuted){window.BOOMR=window.BOOMR||{},window.BOOMR.snippetStart=(new Date).getTime(),window.BOOMR.snippetExecuted=!0,window.BOOMR.snippetVersion=12,window.BOOMR.url=n+"ZUQPP-8TEYN-A7YX5-VYWRZ-Z8K5D";var i=document.currentScript||document.getElementsByTagName("script")[0],o=!1,r=document.createElement("link");if(r.relList&&"function"==typeof r.relList.supports&&r.relList.supports("preload")&&"as"in r)window.BOOMR.snippetMethod="p",r.href=window.BOOMR.url,r.rel="preload",r.as="script",r.addEventListener("load",e),r.addEventListener("error",function(){t(!0)}),setTimeout(function(){if(!o)t(!0)},3e3),BOOMR_lstart=(new Date).getTime(),i.parentNode.appendChild(r);else t(!1);if(window.addEventListener)window.addEventListener("load",a,!1);else if(window.attachEvent)window.attachEvent("onload",a)}}(),"".length>0)if(e&&"performance"in e&&e.performance&&"function"==typeof e.performance.setResourceTimingBufferSize)e.performance.setResourceTimingBufferSize();!function(){if(BOOMR=e.BOOMR||{},BOOMR.plugins=BOOMR.plugins||{},!BOOMR.plugins.AK){var n="true"=="true"?1:0,t="cookiepresent",a="xzvrtpqximpui2ewosrq-f-5fba0ec05-clientnsv4-s.akamaihd.net",i="false"=="true"?2:1,o={"ak.v":"39","ak.cp":"310481","ak.ai":parseInt("190441",10),"ak.ol":"0","ak.cr":16,"ak.ipv":4,"ak.proto":"h2","ak.rid":"310e79c","ak.r":51585,"ak.a2":n,"ak.m":"a","ak.n":"essl","ak.bpcip":"190.107.25.0","ak.cport":61678,"ak.gh":"2.19.211.76","ak.quicv":"","ak.tlsv":"tls1.3","ak.0rtt":"","ak.0rtt.ed":"","ak.csrc":"-","ak.acc":"","ak.t":"1754690723","ak.ak":"hOBiQwZUYzCg5VSAfCLimQ==mIJ1ZJuhsXX2bDFQDpqH9NbQgWF1yre9aMV6pcSOf/h5A5Okj6wv5xdW5f8jNvS1xTH8q2w59i7ECC/Vx8Y9kOjA0+nzKliF4U2yyhI3WwZtsX9YmlselEAi1lLBfkPvMAr3B8PqJWQBfCZgfP52wFE1en/hG5lXAhSKxxjy+t39AoFPYbsPUpzfvhiqqJGs77Am+lCB9HSwoBrv4NBbDX3RA5fERIZ5gt+rCNh3ea0dBXwT04EFD/RQNMJOspjID019KJtra7h2g+KhDkXYQpNUmLupyE7DdIM65a8HTo9an5Hnyw8sSh3Om9AtspbEH19Z+8u7gATt0YF/x+ZWeGVOPBUulKxtdG3WOimxofSSLPtSJNFX/7OdpjLDucjQSAJ84HotFkabiIz7Wdp6G66konAbEAYqsGsWzlt0zms=","ak.pv":"141","ak.dpoabenc":"","ak.tf":i};if(""!==t)o["ak.ruds"]=t;var r={i:!1,av:function(n){var t="http.initiator";if(n&&(!n[t]||"spa_hard"===n[t]))o["ak.feo"]=void 0!==e.aFeoApplied?1:0,BOOMR.addVar(o)},rv:function(){var e=["ak.bpcip","ak.cport","ak.cr","ak.csrc","ak.gh","ak.ipv","ak.m","ak.n","ak.ol","ak.proto","ak.quicv","ak.tlsv","ak.0rtt","ak.0rtt.ed","ak.r","ak.acc","ak.t","ak.tf"];BOOMR.removeVar(e)}};BOOMR.plugins.AK={akVars:o,akDNSPreFetchDomain:a,init:function(){if(!r.i){var e=BOOMR.subscribe;e("before_beacon",r.av,null,null),e("onbeacon",r.rv,null,null),r.i=!0}return this},is_complete:function(){return!0}}}}()}(window);</script>
        <style>
            
        </style>
        
                    <div style="display:none" data-script-portlet-original-tag="head"><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no,maximum-scale=1,user-scalable=0"><meta name="apple-mobile-web-app-capable" content="yes"><link rel="icon" href="favicon.ico"><link rel="stylesheet" href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=jquery-ui.min.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_"><link rel="stylesheet" href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=jquery-ui.structure.min.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_"><link rel="stylesheet" href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=jquery-ui.theme.min.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_"><link rel="stylesheet" href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=toolkit.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_"><link rel="preconnect" href="https://dev.visualwebsiteoptimizer.com"><script id="vwoCode">window._vwo_code=window._vwo_code || (function() {
        var account_id=758416,
        version = 1.5,
        settings_tolerance=2000,
        library_tolerance=2500,
        use_existing_jquery=false,
        is_spa=1,
        hide_element='body',
        hide_element_style = 'opacity:0 !important;filter:alpha(opacity=0) !important;background:none !important',
        /* DO NOT EDIT BELOW THIS LINE */
        f=false,w=window,d=document,vwoCodeEl=d.querySelector('#vwoCode'),code={use_existing_jquery:function(){return use_existing_jquery},library_tolerance:function(){return library_tolerance},hide_element_style:function(){return'{'+hide_element_style+'}'},finish:function(){if(!f){f=true;var e=d.getElementById('_vis_opt_path_hides');if(e)e.parentNode.removeChild(e)}},finished:function(){return f},load:function(e){var t=d.createElement('script');t.fetchPriority='high';t.src=e;t.type='text/javascript';t.onerror=function(){_vwo_code.finish()};d.getElementsByTagName('head')[0].appendChild(t)},getVersion:function(){return version},getMatchedCookies:function(e){var t=[];if(document.cookie){t=document.cookie.match(e)||[]}return t},getCombinationCookie:function(){var e=code.getMatchedCookies(/(?:^|;)\s?(_vis_opt_exp_\d+_combi=[^;$]*)/gi);e=e.map(function(e){try{var t=decodeURIComponent(e);if(!/_vis_opt_exp_\d+_combi=(?:\d+,?)+\s*$/.test(t)){return''}return t}catch(e){return''}});var i=[];e.forEach(function(e){var t=e.match(/([\d,]+)/g);t&&i.push(t.join('-'))});return i.join('|')},init:function(){if(d.URL.indexOf('__vwo_disable__')>-1)return;w.settings_timer=setTimeout(function(){_vwo_code.finish()},settings_tolerance);var e=d.currentScript,t=d.createElement('style'),i=e&&!e.async?hide_element?hide_element+'{'+hide_element_style+'}':'':code.lA=1,n=d.getElementsByTagName('head')[0];t.setAttribute('id','_vis_opt_path_hides');vwoCodeEl&&t.setAttribute('nonce',vwoCodeEl.nonce);t.setAttribute('type','text/css');if(t.styleSheet)t.styleSheet.cssText=i;else t.appendChild(d.createTextNode(i));n.appendChild(t);var o=this.getCombinationCookie();this.load('https://dev.visualwebsiteoptimizer.com/j.php?a='+account_id+'&u='+encodeURIComponent(d.URL)+'&f='+ +is_spa+'&vn='+version+(o?'&c='+o:''));return settings_timer}};w._vwo_settings_timer = code.init();return code;}());</script><title>Auto Incripción</title><link href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=css%2Fapp.81b1270d.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_" rel="preload" as="style"><link href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=css%2Fchunk-vendors.e935173d.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_" rel="preload" as="style"><link href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=js%2Fapp.63fc18aa.js&amp;source=content&amp;subtype=javascript&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_" rel="preload" as="script"><link href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=js%2Fchunk-vendors.78e4ddae.js&amp;source=content&amp;subtype=javascript&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_" rel="preload" as="script"><link href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=css%2Fchunk-vendors.e935173d.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_" rel="stylesheet"><link href="https://www.negocioleonisa.com/wps/wcm/connect/recursos_compartidos/contenido-paises/auto-inscripcion/sp-autoinscripcion-dos-pasos?SRV=cmpnt&amp;cmpntname=css%2Fapp.81b1270d.css&amp;source=content&amp;subtype=css&amp;__SPNS__=ns_Z7_9HK81282N8OQ70QD09V443RGM5_" rel="stylesheet"></div><div data-script-portlet-original-tag="body"><noscript><strong>We're sorry but self-registration-web-frontend doesn't work properly without JavaScript enabled. Please enable it to continue.</strong></noscript><div id="app" class="Grid Grid--alignCenter u-size12of12 u-padSides04 u-md-padSides06 u-lg-padLeft03 u-lg-padRight03"><div class="Grid-cell u-size12of12"><div class="Grid Grid--alignCenter u-padTop02 u-padBottom02"><div class="Grid-cell"><div class="Grid Grid--alignCenter"><div class="Grid-cell"><div class="Grid Grid--alignCenter Grid--alignMiddle u-padTop02 u-padBottom02 PageGirdle js-PageGirdle"><div class="Grid-cell u-size3of12"><div><div class="u-flex u-sizeFull PageGirdle-headerTop Grid--alignRight"><!----><svg width="52" height="52" viewBox="0 0 52 52" class="Icon u-textGrow5"><circle cx="26" cy="26" r="24" stroke-width="2" vector-effect="non-scaling-stroke" fill="none" class="u-textGreen"></circle><svg width="52" height="52" viewBox="0 0 52 52" y="0" x="0" class="Icon u-textSize4 u-textBold u-textGreen"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" x="34"><circle cx="9" cy="9" r="9" fill="#8EC549"></circle><g clip-path="url(#clip0_108_670)"><path d="M9.1626 14.0004C8.52024 14.0004 7.89342 13.887 7.29686 13.6627C6.67413 13.4285 6.11084 13.0841 5.6228 12.6387C5.13476 12.1934 4.7461 11.6696 4.46773 11.0818C4.17954 10.4731 4.0229 9.82246 4.00232 9.14806C3.98173 8.47352 4.09843 7.81507 4.34899 7.19093C4.59096 6.58829 4.94691 6.04317 5.407 5.57088C5.8671 5.09845 6.4083 4.72246 7.01576 4.45307C7.6449 4.17405 8.31725 4.02259 9.01428 4.00267C9.86494 3.97827 10.7146 4.15874 11.4714 4.52444C11.7408 4.65465 11.8502 4.97154 11.7157 5.23236C11.5811 5.49304 11.2537 5.59898 10.9842 5.46877C10.3879 5.18064 9.71812 5.03856 9.04659 5.05769C7.95831 5.08882 6.9476 5.52813 6.20082 6.29489C5.45403 7.06151 5.06046 8.06389 5.09264 9.11705C5.12481 10.1702 5.57877 11.1482 6.37109 11.871C7.1634 12.5937 8.19906 12.9746 9.28733 12.9436C10.374 12.9126 11.3836 12.4742 12.1302 11.7093C12.8766 10.9445 13.2713 9.94423 13.2416 8.89291C13.2332 8.60162 13.4706 8.35887 13.7717 8.35096C13.7768 8.35083 13.7819 8.35069 13.787 8.35069C14.0812 8.35069 14.3237 8.57748 14.3317 8.86389C14.3508 9.53724 14.2332 10.1945 13.9819 10.8173C13.7393 11.4188 13.3831 11.9627 12.9231 12.4339C12.4631 12.9052 11.9222 13.2805 11.3156 13.5491C10.6871 13.8273 10.0156 13.9785 9.31964 13.9985C9.26743 13.9999 9.21508 14.0007 9.16301 14.0007L9.1626 14.0004Z" fill="white"></path><path d="M9.13985 10.9221C9.13072 10.9221 9.12145 10.9218 9.11218 10.9214C8.96113 10.9141 8.8199 10.8463 8.72256 10.7341L6.62317 8.31947C6.42932 8.09652 6.4589 7.76353 6.68929 7.57593C6.91967 7.38834 7.26376 7.41696 7.45761 7.63992L9.1802 9.62119L14.0753 5.02778C14.2915 4.82488 14.6367 4.83002 14.8464 5.03926C15.056 5.24849 15.0507 5.58253 14.8345 5.78543L9.51938 10.7733C9.41741 10.8689 9.28108 10.9221 9.13985 10.9221Z" fill="white"></path></g><defs><clipPath id="clip0_108_670"><rect width="11" height="10" fill="white" transform="translate(4 4)"></rect></clipPath></defs></svg><text x="15" y="40" class="u-hidden u-md-block">1</text><text x="17" y="38" class="u-md-hidden u-block">1</text></svg></svg></div><!----><p class="u-textCenter u-textShrink1 PageGirdle-headerBottom u-borderTopNone"></p></div></div><div class="Grid-cell u-size1of24 u-textGreen"><hr class="u-textGreen u-bgGreen" style="height: 2px; border-width: 0px;"></div><div class="Grid-cell u-size3of12"><div><div class="u-flex u-sizeFull PageGirdle-headerTop Grid--alignLeftCell"><svg width="52" height="52" viewBox="0 0 52 52" class="Icon u-textGrow7 u-textGreen"><circle cx="26" cy="26" r="24" stroke-width="1" vector-effect="non-scaling-stroke"></circle><svg width="52" height="52" viewBox="0 0 52 52" y="0" x="0" class="Icon u-textBlack u-textSize4 u-textBold"><text x="15" y="40" class="u-hidden u-md-block">2</text><text x="16" y="38" class="u-md-hidden u-block">2</text></svg></svg><!----></div><p class="u-textCenter u-textShrink1 PageGirdle-headerBottom u-borderTopNone u-textBlack"></p><!----></div></div></div></div></div><div class="Grid Grid--alignCenter"><div class="Grid-cell u-hidden u-md-block"><div class="Theme u-pad01"><h3 class="u-textBlack u-textCenter">Información de vivienda</h3></div></div><div class="Grid-cell u-md-hidden u-block u-pad01"><h3 class="u-textBlack u-textCenter">Información de vivienda</h3></div></div><!----><div class="Grid u-padTop05 Grid--alignCenter"><div class="Grid-cell u-md-size12of12"><div class="u-flex Grid--alignCenter"><svg width="49" height="29" viewBox="0 0 49 29" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_131_2838)"><path d="M9.19647 28.9451H40.143C40.5708 28.9451 40.918 28.5973 40.918 28.1689V12.4063C40.918 11.9779 40.5708 11.6301 40.143 11.6301C39.7152 11.6301 39.3681 11.9779 39.3681 12.4063V27.3927H9.97143V12.4063C9.97143 11.9779 9.62425 11.6301 9.19647 11.6301C8.7687 11.6301 8.42152 11.9779 8.42152 12.4063V28.1689C8.42152 28.5973 8.7687 28.9451 9.19647 28.9451Z" fill="#333333"></path><path d="M9.45418 12.8028C11.5631 12.8028 13.2783 11.1035 13.2783 9.01606C13.2783 8.58761 12.9311 8.23988 12.5034 8.23988C12.0756 8.23988 11.7284 8.58761 11.7284 9.01606C11.7284 10.2486 10.7086 11.2504 9.45418 11.2504C8.19978 11.2504 7.22334 10.2476 7.22334 9.01606V6.88623L13.2566 1.55339H36.1974L41.745 6.8676V9.01606C41.745 10.2486 40.7438 11.2504 39.5142 11.2504C38.2846 11.2504 37.2833 10.2476 37.2833 9.01606C37.2833 8.58761 36.9362 8.23988 36.5084 8.23988C36.0806 8.23988 35.7334 8.58761 35.7334 9.01606C35.7334 11.1045 37.429 12.8028 39.5142 12.8028C41.5993 12.8028 43.2949 11.1035 43.2949 9.01606V6.5354C43.2949 6.32325 43.2081 6.12144 43.0552 5.97448L37.0436 0.215259C36.899 0.0776176 36.7078 0 36.5084 0H12.9632C12.7741 0 12.5922 0.0693384 12.4507 0.194561L5.93588 5.95379C5.76953 6.10074 5.67343 6.3129 5.67343 6.5354V9.01606C5.67343 11.1045 7.36903 12.8028 9.45418 12.8028Z" fill="#333333"></path><path d="M33.5025 12.8029C35.5876 12.8029 37.2832 11.1036 37.2832 9.01617C37.2832 8.58772 36.936 8.23999 36.5082 8.23999C36.0805 8.23999 35.7333 8.58772 35.7333 9.01617C35.7333 10.2487 34.7321 11.2505 33.5025 11.2505C32.2729 11.2505 31.2716 10.2477 31.2716 9.01617C31.2716 8.58772 30.9244 8.23999 30.4967 8.23999C30.0689 8.23999 29.7217 8.58772 29.7217 9.01617C29.7217 11.1046 31.4173 12.8029 33.5025 12.8029Z" fill="#333333"></path><path d="M27.4898 12.8029C29.5749 12.8029 31.2705 11.1036 31.2705 9.01617C31.2705 8.58772 30.9233 8.23999 30.4956 8.23999C30.0678 8.23999 29.7206 8.58772 29.7206 9.01617C29.7206 10.2487 28.7194 11.2505 27.4898 11.2505C26.2602 11.2505 25.2589 10.2477 25.2589 9.01617C25.2589 8.58772 24.9117 8.23999 24.484 8.23999C24.0562 8.23999 23.709 8.58772 23.709 9.01617C23.709 11.1046 25.4046 12.8029 27.4898 12.8029Z" fill="#333333"></path><path d="M21.478 12.8029C23.5632 12.8029 25.2588 11.1036 25.2588 9.01617C25.2588 8.58772 24.9116 8.23999 24.4838 8.23999C24.0561 8.23999 23.7089 8.58772 23.7089 9.01617C23.7089 10.2487 22.7076 11.2505 21.478 11.2505C20.2484 11.2505 19.271 10.2477 19.271 9.01617C19.271 8.58772 18.9238 8.23999 18.496 8.23999C18.0682 8.23999 17.7211 8.58772 17.7211 9.01617C17.7211 11.1046 19.4063 12.8029 21.478 12.8029Z" fill="#333333"></path><path d="M15.467 12.8029C17.5655 12.8029 19.2715 11.1036 19.2715 9.01617C19.2715 8.58772 18.9243 8.23999 18.4965 8.23999C18.0688 8.23999 17.7216 8.58772 17.7216 9.01617C17.7216 10.2487 16.71 11.2505 15.467 11.2505C14.2239 11.2505 13.2785 10.2694 13.2785 9.01617C13.2785 8.58772 12.9313 8.23999 12.5035 8.23999C12.0758 8.23999 11.7286 8.58772 11.7286 9.01617C11.7286 11.1046 13.4056 12.8029 15.467 12.8029Z" fill="#333333"></path><path d="M27.2787 28.5343C27.7065 28.5343 28.0537 28.1866 28.0537 27.7581V17.7196H32.9101V27.7581C32.9101 28.1866 33.2572 28.5343 33.685 28.5343C34.1128 28.5343 34.46 28.1866 34.46 27.7581V16.9434C34.46 16.515 34.1128 16.1672 33.685 16.1672H27.2787C26.8509 16.1672 26.5038 16.515 26.5038 16.9434V27.7581C26.5038 28.1866 26.8509 28.5343 27.2787 28.5343Z" fill="#333333"></path><path d="M15.8993 22.8143H20.9623C21.3901 22.8143 21.7373 22.4666 21.7373 22.0381V16.9671C21.7373 16.5386 21.3901 16.1909 20.9623 16.1909H15.8993C15.4715 16.1909 15.1244 16.5386 15.1244 16.9671V22.0381C15.1244 22.4666 15.4715 22.8143 15.8993 22.8143ZM20.1874 21.2619H16.6743V17.7433H20.1874V21.2619Z" fill="#333333"></path><path d="M36.475 9.80248C36.9028 9.80248 37.25 9.45475 37.25 9.0263V6.40076C37.25 6.24759 37.2045 6.0965 37.1188 5.96921L36.2653 4.6911C36.0276 4.3351 35.5461 4.23885 35.1907 4.47791C34.8352 4.71594 34.7391 5.19821 34.9778 5.55421L35.7011 6.63672V9.0263C35.7011 9.45475 36.0483 9.80248 36.4761 9.80248H36.475Z" fill="#333333"></path><path d="M30.4819 9.80265C30.9097 9.80265 31.2568 9.45492 31.2568 9.02647V6.40093C31.2568 6.32642 31.2465 6.2519 31.2248 6.18049L30.8466 4.90239C30.7247 4.49154 30.2938 4.25661 29.8836 4.37873C29.4734 4.50085 29.2389 4.9324 29.3608 5.34326L29.7069 6.51373V9.02647C29.7069 9.45492 30.0541 9.80265 30.4819 9.80265Z" fill="#333333"></path><path d="M12.5038 9.80263C12.9316 9.80263 13.2788 9.45491 13.2788 9.02646V6.64618L14.0341 5.56885C14.28 5.21802 14.1953 4.73369 13.845 4.48738C13.4947 4.24107 13.0111 4.32594 12.7652 4.67677L11.8683 5.95487C11.7764 6.08527 11.7278 6.24154 11.7278 6.40091V9.02646C11.7278 9.45491 12.075 9.80263 12.5028 9.80263H12.5038Z" fill="#333333"></path><path d="M18.4964 9.8026C18.9242 9.8026 19.2713 9.45487 19.2713 9.02643V6.52403L19.6475 5.36184C19.7797 4.95409 19.5565 4.51633 19.1494 4.38386C18.7423 4.25139 18.3052 4.47493 18.173 4.88268L17.7586 6.16078C17.7338 6.2384 17.7204 6.31912 17.7204 6.40088V9.02643C17.7204 9.45487 18.0676 9.8026 18.4953 9.8026H18.4964Z" fill="#333333"></path><path d="M24.4897 9.8026C24.9175 9.8026 25.2646 9.45488 25.2646 9.02643V5.0938C25.2646 4.66535 24.9175 4.31763 24.4897 4.31763C24.0619 4.31763 23.7147 4.66535 23.7147 5.0938V9.02643C23.7147 9.45488 24.0619 9.8026 24.4897 9.8026Z" fill="#333333"></path><path d="M0.775364 29.0001H47.686C48.1138 29.0001 48.4609 28.6524 48.4609 28.2239C48.4609 27.7955 48.1138 27.4478 47.686 27.4478H0.775364C0.347588 27.4478 0.000408173 27.7955 0.000408173 28.2239C0.000408173 28.6524 0.347588 29.0001 0.775364 29.0001Z" fill="#333333"></path><path d="M3.41009 28.8416C3.60848 28.8416 3.80686 28.766 3.95772 28.6139C4.26047 28.3107 4.26047 27.8191 3.95772 27.5159C3.59711 27.1547 3.39872 26.6745 3.39872 26.1633C3.39872 25.1749 4.16851 24.3377 5.15115 24.257C5.55826 24.2238 5.86928 23.8803 5.86308 23.4715C5.86308 23.4694 5.86308 23.4673 5.86308 23.4653C5.86824 22.6404 6.53987 21.9698 7.36442 21.9698C7.69197 21.9698 8.00195 22.0733 8.26337 22.2689C8.60642 22.5256 9.09206 22.4562 9.34831 22.1126C9.60456 21.7691 9.53533 21.2827 9.19228 21.026C8.66118 20.6276 8.02882 20.4175 7.36442 20.4175C5.90441 20.4175 4.67998 21.4503 4.3824 22.8247C2.92032 23.2355 1.84881 24.5933 1.84881 26.1622C1.84881 27.0874 2.20839 27.9578 2.86245 28.6129C3.01331 28.764 3.2117 28.8405 3.41009 28.8405V28.8416Z" fill="#333333"></path><path d="M5.44525 25.6395L6.31009 24.3511L6.31836 24.3562C6.29666 24.3407 5.78312 23.9661 5.85649 23.3648C5.90815 22.9395 5.6054 22.5524 5.18073 22.5007C4.75502 22.45 4.36961 22.7522 4.31794 23.1775C4.16709 24.4194 4.95547 25.3094 5.44525 25.6395Z" fill="#333333"></path><path d="M45.759 28.8418C45.9574 28.8418 46.1558 28.7662 46.3067 28.6141C46.9597 27.96 47.3203 27.0897 47.3203 26.1634C47.3203 24.5945 46.2498 23.2367 44.7878 22.8259C44.4902 21.4515 43.2657 20.4187 41.8057 20.4187C41.1413 20.4187 40.509 20.6288 39.9779 21.0272C39.6348 21.2839 39.5656 21.7703 39.8218 22.1139C40.0781 22.4575 40.5637 22.5268 40.9068 22.2701C41.1672 22.0745 41.4782 21.9711 41.8057 21.9711C42.6313 21.9711 43.3029 22.6406 43.3071 23.4665C43.3071 23.4727 43.3071 23.4799 43.3071 23.4851C43.3071 23.8898 43.6171 24.2261 44.019 24.2592C45.0016 24.3399 45.7714 25.1761 45.7714 26.1655C45.7714 26.6767 45.573 27.1569 45.2124 27.5181C44.9097 27.8213 44.9097 28.3129 45.2124 28.6162C45.3633 28.7672 45.5617 28.8438 45.7601 28.8438L45.759 28.8418Z" fill="#333333"></path><path d="M43.292 25.7722C43.4408 25.7722 43.5907 25.7298 43.7239 25.6397C44.2137 25.3096 45.0021 24.4206 44.8512 23.1777C44.7996 22.7523 44.4131 22.4491 43.9885 22.5009C43.5638 22.5526 43.261 22.9397 43.3127 23.365C43.3871 23.9766 42.8643 24.3482 42.8591 24.3513C42.5036 24.5903 42.4096 25.0726 42.6483 25.4286C42.7981 25.6511 43.043 25.7722 43.292 25.7722Z" fill="#333333"></path></g><defs><clipPath id="clip0_131_2838"><rect width="48.4605" height="29" fill="white" transform="matrix(-1 0 0 1 48.4609 0)"></rect></clipPath></defs></svg><h4 class="u-padLeft04 u-padTop05">Cuéntanos dónde vives</h4></div></div></div></div><section id="initial-data-validation-wide-modal" aria-hidden="true" class="Modal js-Modal"><div tabindex="-1" role="dialog" class="Modal-overlay"></div><div role="dialog" aria-labelledby="initial-data-validation-wide-modal" class="Modal-dialog"><div role="document" class="Modal-document Thumbnail-object"><div class="Modal-header"></div><div class="Modal-main modal-border-radius-top"><div class="Modal-content u-staggerItems1 u-textCenter"><div class="Grid Grid--alignCenter"><div class="Grid-cell u-md-size11of12 u-lg-size10of12 u-size12of12"><div class="u-textGrow3 u-md-textGrow4 u-lg-textGrow4"><svg width="37" height="44" viewBox="0 0 37 44" fill="none"><path d="M7.21589 8.11803H21.1664C21.5296 8.11803 21.8267 7.82741 21.8267 7.47221C21.8267 3.35184 18.4001 0 14.1879 0C9.97563 0 6.55566 3.35184 6.55566 7.47221C6.55566 7.82741 6.85277 8.11803 7.21589 8.11803ZM14.1879 1.29165C17.4494 1.29165 20.1365 3.71996 20.4666 6.82638H7.90913C8.23924 3.71996 10.933 1.29165 14.1879 1.29165Z" fill="#333333"></path><path d="M18.3477 38.1165H3.07005C2.10612 38.1165 1.32045 37.348 1.32045 36.4051V8.2277C1.32045 7.28479 2.10612 6.51626 3.07005 6.51626H4.00757C4.37069 6.51626 4.66779 6.22564 4.66779 5.87044C4.66779 5.51523 4.37069 5.22461 4.00757 5.22461H3.07005C1.37987 5.22461 0 6.56793 0 8.2277V36.4116C0 38.0649 1.37327 39.4146 3.07005 39.4146H18.3477C18.7108 39.4146 19.0079 39.124 19.0079 38.7688C19.0079 38.4136 18.7108 38.123 18.3477 38.123V38.1165Z" fill="#333333"></path><path d="M24.085 6.51626H25.2668C26.2308 6.51626 27.0164 7.28479 27.0164 8.2277V25.6392C27.0164 25.9944 27.3135 26.285 27.6767 26.285C28.0398 26.285 28.3369 25.9944 28.3369 25.6392V8.2277C28.3369 6.57439 26.9636 5.22461 25.2668 5.22461H24.085C23.7219 5.22461 23.4248 5.51523 23.4248 5.87044C23.4248 6.22564 23.7219 6.51626 24.085 6.51626Z" fill="#333333"></path><path d="M7.18952 14.5827H21.1401C21.5032 14.5827 21.8003 14.292 21.8003 13.9368C21.8003 13.5816 21.5032 13.291 21.1401 13.291H7.18952C6.8264 13.291 6.5293 13.5816 6.5293 13.9368C6.5293 14.292 6.8264 14.5827 7.18952 14.5827Z" fill="#333333"></path><path d="M7.18952 22.9655H21.1401C21.5032 22.9655 21.8003 22.6749 21.8003 22.3197C21.8003 21.9644 21.5032 21.6738 21.1401 21.6738H7.18952C6.8264 21.6738 6.5293 21.9644 6.5293 22.3197C6.5293 22.6749 6.8264 22.9655 7.18952 22.9655Z" fill="#333333"></path><path d="M7.18952 31.3483H18.3473C18.7105 31.3483 19.0076 31.0577 19.0076 30.7025C19.0076 30.3473 18.7105 30.0566 18.3473 30.0566H7.18952C6.8264 30.0566 6.5293 30.3473 6.5293 30.7025C6.5293 31.0577 6.8264 31.3483 7.18952 31.3483Z" fill="#333333"></path><path d="M27.6771 27.2021C22.9763 27.2021 19.1602 30.9415 19.1602 35.5333C19.1602 40.1251 22.9829 43.8645 27.6771 43.8645C32.3713 43.8645 36.194 40.1251 36.194 35.5333C36.194 30.9415 32.3713 27.2021 27.6771 27.2021ZM27.6771 42.5793C23.7091 42.5793 20.4806 39.4212 20.4806 35.5398C20.4806 31.6583 23.7091 28.5003 27.6771 28.5003C31.645 28.5003 34.8735 31.6583 34.8735 35.5398C34.8735 39.4212 31.645 42.5793 27.6771 42.5793Z" fill="#333333"></path><path d="M31.413 32.892L26.5867 37.613L23.9326 35.0168C23.6751 34.7649 23.2592 34.7649 23.0017 35.0168C22.7442 35.2687 22.7442 35.6755 23.0017 35.9274L26.1246 38.9822C26.25 39.1049 26.4151 39.1695 26.5933 39.1695C26.7716 39.1695 26.9367 39.0984 27.0621 38.9822L32.3571 33.8026C32.6146 33.5508 32.6146 33.1439 32.3571 32.892C32.0996 32.6402 31.6837 32.6402 31.4262 32.892H31.413Z" fill="#333333"></path></svg></div><div><h3 class="u-textUpper u-textCenter u-sizeFull u-textSize1 u-md-textSize2 u-lg-textSize1"> ANTES DE CONTINUAR </h3><h1 class="u-textUpper u-textCenter u-sizeFull u-textSize3 u-md-textSize4 u-lg-textSize3"> VERIFICA TUS DATOS </h1><br><br><div class="Grid"><div class="Grid-cell u-size12of12 u-sm-size12of12 u-md-size2of12 u-lg-size2of12"><svg width="49" height="29" viewBox="0 0 49 29" fill="none" xmlns="http://www.w3.org/2000/svg"><g><path d="M9.19647 28.9451H40.143C40.5708 28.9451 40.918 28.5973 40.918 28.1689V12.4063C40.918 11.9779 40.5708 11.6301 40.143 11.6301C39.7152 11.6301 39.3681 11.9779 39.3681 12.4063V27.3927H9.97143V12.4063C9.97143 11.9779 9.62425 11.6301 9.19647 11.6301C8.7687 11.6301 8.42152 11.9779 8.42152 12.4063V28.1689C8.42152 28.5973 8.7687 28.9451 9.19647 28.9451Z" fill="#333333"></path><path d="M9.45418 12.8028C11.5631 12.8028 13.2783 11.1035 13.2783 9.01606C13.2783 8.58761 12.9311 8.23988 12.5034 8.23988C12.0756 8.23988 11.7284 8.58761 11.7284 9.01606C11.7284 10.2486 10.7086 11.2504 9.45418 11.2504C8.19978 11.2504 7.22334 10.2476 7.22334 9.01606V6.88623L13.2566 1.55339H36.1974L41.745 6.8676V9.01606C41.745 10.2486 40.7438 11.2504 39.5142 11.2504C38.2846 11.2504 37.2833 10.2476 37.2833 9.01606C37.2833 8.58761 36.9362 8.23988 36.5084 8.23988C36.0806 8.23988 35.7334 8.58761 35.7334 9.01606C35.7334 11.1045 37.429 12.8028 39.5142 12.8028C41.5993 12.8028 43.2949 11.1035 43.2949 9.01606V6.5354C43.2949 6.32325 43.2081 6.12144 43.0552 5.97448L37.0436 0.215259C36.899 0.0776176 36.7078 0 36.5084 0H12.9632C12.7741 0 12.5922 0.0693384 12.4507 0.194561L5.93588 5.95379C5.76953 6.10074 5.67343 6.3129 5.67343 6.5354V9.01606C5.67343 11.1045 7.36903 12.8028 9.45418 12.8028Z" fill="#333333"></path><path d="M33.5025 12.8029C35.5876 12.8029 37.2832 11.1036 37.2832 9.01617C37.2832 8.58772 36.936 8.23999 36.5082 8.23999C36.0805 8.23999 35.7333 8.58772 35.7333 9.01617C35.7333 10.2487 34.7321 11.2505 33.5025 11.2505C32.2729 11.2505 31.2716 10.2477 31.2716 9.01617C31.2716 8.58772 30.9244 8.23999 30.4967 8.23999C30.0689 8.23999 29.7217 8.58772 29.7217 9.01617C29.7217 11.1046 31.4173 12.8029 33.5025 12.8029Z" fill="#333333"></path><path d="M27.4898 12.8029C29.5749 12.8029 31.2705 11.1036 31.2705 9.01617C31.2705 8.58772 30.9233 8.23999 30.4956 8.23999C30.0678 8.23999 29.7206 8.58772 29.7206 9.01617C29.7206 10.2487 28.7194 11.2505 27.4898 11.2505C26.2602 11.2505 25.2589 10.2477 25.2589 9.01617C25.2589 8.58772 24.9117 8.23999 24.484 8.23999C24.0562 8.23999 23.709 8.58772 23.709 9.01617C23.709 11.1046 25.4046 12.8029 27.4898 12.8029Z" fill="#333333"></path><path d="M21.478 12.8029C23.5632 12.8029 25.2588 11.1036 25.2588 9.01617C25.2588 8.58772 24.9116 8.23999 24.4838 8.23999C24.0561 8.23999 23.7089 8.58772 23.7089 9.01617C23.7089 10.2487 22.7076 11.2505 21.478 11.2505C20.2484 11.2505 19.271 10.2477 19.271 9.01617C19.271 8.58772 18.9238 8.23999 18.496 8.23999C18.0682 8.23999 17.7211 8.58772 17.7211 9.01617C17.7211 11.1046 19.4063 12.8029 21.478 12.8029Z" fill="#333333"></path><path d="M15.467 12.8029C17.5655 12.8029 19.2715 11.1036 19.2715 9.01617C19.2715 8.58772 18.9243 8.23999 18.4965 8.23999C18.0688 8.23999 17.7216 8.58772 17.7216 9.01617C17.7216 10.2487 16.71 11.2505 15.467 11.2505C14.2239 11.2505 13.2785 10.2694 13.2785 9.01617C13.2785 8.58772 12.9313 8.23999 12.5035 8.23999C12.0758 8.23999 11.7286 8.58772 11.7286 9.01617C11.7286 11.1046 13.4056 12.8029 15.467 12.8029Z" fill="#333333"></path><path d="M27.2787 28.5343C27.7065 28.5343 28.0537 28.1866 28.0537 27.7581V17.7196H32.9101V27.7581C32.9101 28.1866 33.2572 28.5343 33.685 28.5343C34.1128 28.5343 34.46 28.1866 34.46 27.7581V16.9434C34.46 16.515 34.1128 16.1672 33.685 16.1672H27.2787C26.8509 16.1672 26.5038 16.515 26.5038 16.9434V27.7581C26.5038 28.1866 26.8509 28.5343 27.2787 28.5343Z" fill="#333333"></path><path d="M15.8993 22.8143H20.9623C21.3901 22.8143 21.7373 22.4666 21.7373 22.0381V16.9671C21.7373 16.5386 21.3901 16.1909 20.9623 16.1909H15.8993C15.4715 16.1909 15.1244 16.5386 15.1244 16.9671V22.0381C15.1244 22.4666 15.4715 22.8143 15.8993 22.8143ZM20.1874 21.2619H16.6743V17.7433H20.1874V21.2619Z" fill="#333333"></path><path d="M36.475 9.80248C36.9028 9.80248 37.25 9.45475 37.25 9.0263V6.40076C37.25 6.24759 37.2045 6.0965 37.1188 5.96921L36.2653 4.6911C36.0276 4.3351 35.5461 4.23885 35.1907 4.47791C34.8352 4.71594 34.7391 5.19821 34.9778 5.55421L35.7011 6.63672V9.0263C35.7011 9.45475 36.0483 9.80248 36.4761 9.80248H36.475Z" fill="#333333"></path><path d="M30.4819 9.80265C30.9097 9.80265 31.2568 9.45492 31.2568 9.02647V6.40093C31.2568 6.32642 31.2465 6.2519 31.2248 6.18049L30.8466 4.90239C30.7247 4.49154 30.2938 4.25661 29.8836 4.37873C29.4734 4.50085 29.2389 4.9324 29.3608 5.34326L29.7069 6.51373V9.02647C29.7069 9.45492 30.0541 9.80265 30.4819 9.80265Z" fill="#333333"></path><path d="M12.5038 9.80263C12.9316 9.80263 13.2788 9.45491 13.2788 9.02646V6.64618L14.0341 5.56885C14.28 5.21802 14.1953 4.73369 13.845 4.48738C13.4947 4.24107 13.0111 4.32594 12.7652 4.67677L11.8683 5.95487C11.7764 6.08527 11.7278 6.24154 11.7278 6.40091V9.02646C11.7278 9.45491 12.075 9.80263 12.5028 9.80263H12.5038Z" fill="#333333"></path><path d="M18.4964 9.8026C18.9242 9.8026 19.2713 9.45487 19.2713 9.02643V6.52403L19.6475 5.36184C19.7797 4.95409 19.5565 4.51633 19.1494 4.38386C18.7423 4.25139 18.3052 4.47493 18.173 4.88268L17.7586 6.16078C17.7338 6.2384 17.7204 6.31912 17.7204 6.40088V9.02643C17.7204 9.45487 18.0676 9.8026 18.4953 9.8026H18.4964Z" fill="#333333"></path><path d="M24.4897 9.8026C24.9175 9.8026 25.2646 9.45488 25.2646 9.02643V5.0938C25.2646 4.66535 24.9175 4.31763 24.4897 4.31763C24.0619 4.31763 23.7147 4.66535 23.7147 5.0938V9.02643C23.7147 9.45488 24.0619 9.8026 24.4897 9.8026Z" fill="#333333"></path><path d="M0.775364 29.0001H47.686C48.1138 29.0001 48.4609 28.6524 48.4609 28.2239C48.4609 27.7955 48.1138 27.4478 47.686 27.4478H0.775364C0.347588 27.4478 0.000408173 27.7955 0.000408173 28.2239C0.000408173 28.6524 0.347588 29.0001 0.775364 29.0001Z" fill="#333333"></path><path d="M3.41009 28.8416C3.60848 28.8416 3.80686 28.766 3.95772 28.6139C4.26047 28.3107 4.26047 27.8191 3.95772 27.5159C3.59711 27.1547 3.39872 26.6745 3.39872 26.1633C3.39872 25.1749 4.16851 24.3377 5.15115 24.257C5.55826 24.2238 5.86928 23.8803 5.86308 23.4715C5.86308 23.4694 5.86308 23.4673 5.86308 23.4653C5.86824 22.6404 6.53987 21.9698 7.36442 21.9698C7.69197 21.9698 8.00195 22.0733 8.26337 22.2689C8.60642 22.5256 9.09206 22.4562 9.34831 22.1126C9.60456 21.7691 9.53533 21.2827 9.19228 21.026C8.66118 20.6276 8.02882 20.4175 7.36442 20.4175C5.90441 20.4175 4.67998 21.4503 4.3824 22.8247C2.92032 23.2355 1.84881 24.5933 1.84881 26.1622C1.84881 27.0874 2.20839 27.9578 2.86245 28.6129C3.01331 28.764 3.2117 28.8405 3.41009 28.8405V28.8416Z" fill="#333333"></path><path d="M5.44525 25.6395L6.31009 24.3511L6.31836 24.3562C6.29666 24.3407 5.78312 23.9661 5.85649 23.3648C5.90815 22.9395 5.6054 22.5524 5.18073 22.5007C4.75502 22.45 4.36961 22.7522 4.31794 23.1775C4.16709 24.4194 4.95547 25.3094 5.44525 25.6395Z" fill="#333333"></path><path d="M45.759 28.8418C45.9574 28.8418 46.1558 28.7662 46.3067 28.6141C46.9597 27.96 47.3203 27.0897 47.3203 26.1634C47.3203 24.5945 46.2498 23.2367 44.7878 22.8259C44.4902 21.4515 43.2657 20.4187 41.8057 20.4187C41.1413 20.4187 40.509 20.6288 39.9779 21.0272C39.6348 21.2839 39.5656 21.7703 39.8218 22.1139C40.0781 22.4575 40.5637 22.5268 40.9068 22.2701C41.1672 22.0745 41.4782 21.9711 41.8057 21.9711C42.6313 21.9711 43.3029 22.6406 43.3071 23.4665C43.3071 23.4727 43.3071 23.4799 43.3071 23.4851C43.3071 23.8898 43.6171 24.2261 44.019 24.2592C45.0016 24.3399 45.7714 25.1761 45.7714 26.1655C45.7714 26.6767 45.573 27.1569 45.2124 27.5181C44.9097 27.8213 44.9097 28.3129 45.2124 28.6162C45.3633 28.7672 45.5617 28.8438 45.7601 28.8438L45.759 28.8418Z" fill="#333333"></path><path d="M43.292 25.7722C43.4408 25.7722 43.5907 25.7298 43.7239 25.6397C44.2137 25.3096 45.0021 24.4206 44.8512 23.1777C44.7996 22.7523 44.4131 22.4491 43.9885 22.5009C43.5638 22.5526 43.261 22.9397 43.3127 23.365C43.3871 23.9766 42.8643 24.3482 42.8591 24.3513C42.5036 24.5903 42.4096 25.0726 42.6483 25.4286C42.7981 25.6511 43.043 25.7722 43.292 25.7722Z" fill="#333333"></path></g><defs><clipPath id="clip0_131_3461"><rect width="48.4605" height="29" fill="white" transform="matrix(-1 0 0 1 48.4609 0)"></rect></clipPath></defs></svg></div><div class="Grid-cell u-size12of12 u-sm-size12of12 u-md-size10of12 u-lg-size10of12"><p class="u-textBold u-textCenter u-md-textLeft u-lg-textLeft"> Dirección de vivienda: </p><p class="u-textCenter u-md-textLeft u-lg-textLeft u-textMercury">  , ,  </p></div></div><div class="Grid u-spaceBottom06 u-spaceTop06"><div class="Grid-cell u-size1of12 u-sm-size1of12 u-md-size2of12 u-lg-size2of12"></div><div class="Grid-cell u-size10of12 u-sm-size10of12 u-md-size5of12 u-lg-size5of12"><hr class="u-textBlack u-bgBlack" style="height: 2px; border-width: 0px;"></div><div class="Grid-cell u-size1of12 u-sm-size1of12 u-md-size5of12 u-lg-size5of12"></div></div><div class="Grid"><div class="Grid-cell u-size12of12 u-sm-size12of12 u-md-size2of12 u-lg-size2of12"><svg width="30" height="36" viewBox="0 0 30 36" fill="none" xmlns="http://www.w3.org/2000/svg"><g><path d="M15.0002 31.1218C14.8314 31.1218 14.6626 31.0565 14.534 30.9265C10.2525 26.5985 6.88941 21.5557 4.53814 15.9414C3.94635 14.5256 3.64648 13.023 3.64648 11.4727C3.64648 9.92249 3.94635 8.4199 4.53814 7.00515C5.11156 5.63606 5.93073 4.409 6.97132 3.35759C8.01341 2.30367 9.22776 1.4756 10.5806 0.897447C13.3802 -0.298498 16.6207 -0.298498 19.4202 0.897447C20.7721 1.47459 21.986 2.30267 23.029 3.35759C24.0711 4.4105 24.8898 5.63806 25.4617 7.00515C26.054 8.4194 26.3544 9.92249 26.3544 11.4727C26.3544 13.023 26.054 14.5266 25.4612 15.9414C23.11 21.5577 19.7474 26.5995 15.4669 30.9265C15.3378 31.0565 15.1695 31.1218 15.0007 31.1218H15.0002ZM15.0002 1.32855C13.6443 1.32855 12.3302 1.59654 11.094 2.12551C9.89849 2.63591 8.82563 3.36763 7.90418 4.30009C6.98324 5.22955 6.25989 6.31508 5.7525 7.52508C5.23021 8.77422 4.9651 10.1022 4.9651 11.4727C4.9651 12.8433 5.23021 14.1723 5.75299 15.4214C7.95135 20.6724 11.0607 25.4085 15.0002 29.5058C18.9387 25.4085 22.0475 20.6744 24.2464 15.4209C24.7697 14.1728 25.0353 12.8443 25.0353 11.4733C25.0353 10.1022 24.7702 8.77372 24.2469 7.52558C23.741 6.31659 23.0176 5.23206 22.0957 4.3016C21.1733 3.36863 20.1004 2.63691 18.9064 2.12651C17.6702 1.59805 16.356 1.32955 15.0002 1.32955V1.32855Z" fill="#333333"></path><path d="M14.9999 16.2872C12.3741 16.2872 10.2373 14.1277 10.2373 11.4728C10.2373 8.81797 12.3736 6.65845 14.9999 6.65845C17.6262 6.65845 19.7625 8.81797 19.7625 11.4728C19.7625 14.1277 17.6262 16.2872 14.9999 16.2872ZM14.9999 7.9919C13.1014 7.9919 11.5564 9.55371 11.5564 11.4728C11.5564 13.392 13.1014 14.9538 14.9999 14.9538C16.8984 14.9538 18.4434 13.392 18.4434 11.4728C18.4434 9.55371 16.8984 7.9919 14.9999 7.9919Z" fill="#333333"></path><path d="M21.2905 26.0735C20.9936 26.485 20.6883 26.891 20.378 27.295C25.6177 27.9088 28.6809 29.3482 28.6809 30.4558C28.6809 31.9022 23.4764 33.9177 14.9998 33.9177C6.52308 33.9177 1.31911 31.9012 1.31911 30.4553C1.31911 29.3477 4.38231 27.9083 9.62202 27.2945C9.31223 26.891 9.0064 26.4845 8.70952 26.073C3.82279 26.741 0 28.2155 0 30.4553C0 33.603 7.5458 35.2506 15.0002 35.2506C22.4547 35.2506 30 33.603 30 30.4553C30 28.216 26.1772 26.741 21.2905 26.0735Z" fill="#333333"></path></g><defs><clipPath id="clip0_131_3499"><rect width="30" height="35.25" fill="white"></rect></clipPath></defs></svg></div><div class="Grid-cell u-size12of12 u-sm-size12of12 u-md-size10of12 u-lg-size10of12"><p class="u-textBold u-textCenter u-md-textLeft u-lg-textLeft"> Dirección de envío: </p><p class="u-textCenter u-md-textLeft u-lg-textLeft u-textMercury">  , ,  </p></div></div></div></div></div></div></div><div class="Modal-footer u-hidden u-md-block u-borderTopNone modal-border-radius-bottom"><div class="Grid Grid--alignCenter"><div class="Grid-cell u-md-size11of12 u-lg-size10of12 "><div class="Grid Grid--alignCenter"><div class="Grid-cell u-lg-size5of10 u-md-size5of10 u-padTop01 u-textCenter u-spaceItems1 "><button id="aut_country_p2_mod_modificar" class="Button Button--inverted u-textCapitalize" style="width: 100%;"> Modificar </button></div><div class="Grid-cell u-md-size5of10 u-lg-size5of10  u-padTop01 u-textCenter u-spaceItems1 u-md-padLeft04"><button id="aut_country_p2_mod_confirmar" class="Button Button--success u-textCapitalize" style="width: 100%;"> Confirmar </button></div><div class="Grid-cell "><p class="u-block u-textShrink1 u-textCenter u-size12of12 u-padTop02"> * Ten en cuenta: recuerda revisar muy bien tu dirección de envío antes de continuar para evitar que tus pedidos lleguen a una dirección errada. </p></div></div></div></div></div><div class="Modal-footer u-md-hidden u-block u-borderTopNone modal-border-radius-bottom"><div class="Grid Grid--alignCenter"><div class="Grid-cell  u-size12of12"><div class="Grid Grid--alignCenter"><div class="Grid-cell u-size12of12 u-padTop01 u-textCenter u-spaceItems1 "><button id="aut_country_p2_mod_confirmar" class="Button Button--success u-textCapitalize" style="width: 100%;"> Confirmar </button></div><div class="Grid-cell u-size12of12 u-padTop01 u-textCenter u-spaceItems1 "><button id="aut_country_p2_mod_modificar" class="Button Button--inverted u-textCapitalize" style="width: 100%;"> Modificar </button></div><div class="Grid-cell u-size12of12"><p class="u-block u-textShrink1 u-textCenter u-size12of12 u-padTop02"> * Ten en cuenta: recuerda revisar muy bien tu dirección de envío antes de continuar para evitar que tus pedidos lleguen a una dirección errada. </p></div></div></div></div></div></div></div></section><div><section id="validation-identification-wide-modal" aria-hidden="true" class="Modal js-Modal"><div tabindex="-1" class="Modal-overlay"></div><div role="dialog" aria-labelledby="validation-identification-wide-modal" class="Modal-dialog"><div role="document" class="Modal-document"><div class="Modal-header modal-border-radius-top u-bgWhite u-borderBottomMd u-borderSilver"><h1 id="validation-identification-wide-modal" class="Modal-title u-textUpper u-textCenter u-sizeFull u-textBlack"> Importante </h1></div><div class="Modal-main u-borderBottomMd u-borderSilver"><div class="Modal-content u-staggerItems1 u-textCenter"><div class="Grid Grid--alignCenter"><div class="Grid-cell u-md-size10of12"><div class="u-textGrow4"><svg width="26" height="26" viewBox="0 0 26 26" class="Icon Icon--block u-flexExpandSides u-textGrow4 u-spaceEnds06 u-textRed"><path d="M11.25,10.76c.12,1.45.29,2.83.49,4.18h2.55c.19-1.35.34-2.77.47-4.19l.36-4.27H10.88Z M13.05,0a13,13,0,1,0,13,13A13,13,0,0,0,13.05,0Zm0,23.38A10.38,10.38,0,1,1,23.43,13,10.4,10.4,0,0,1,13.05,23.38Z"></path><rect x="11.3" y="15.96" width="3.49" height="3.57"></rect></svg></div></div><div class="Grid-cell u-md-size10of12"><p class="u-padEnds06"></p></div></div></div></div><div class="Modal-footer u-borderTopNone modal-border-radius-bottom"><div class="Grid Grid--alignCenter u-textCenter"><div class="Grid-cell u-md-size10of12"><button id="aut_mod_cerrar_error" class="Button u-textCapitalize Button--success u-spaceSides01"> Cerrar </button></div></div></div></div></div></section></div></div></div></div><script>// Picture element HTML5 shiv
            document.createElement("picture");</script></div>
            <script>
                    
            </script>
        
    <div class="wpthemeClear"></div>
        </div>
    </section>
    </div></div><div style="clear:both"></div>
    </div>

    <script type="text/javascript">
        $.each($("div.component-control"), function(index, it) {
            var $i = $(it).find("input[name=class]");
            var $s = $(it).find("input[name=sticky]");
            $(it).addClass($i.length > 0 ? $i.val() : "");
            $(it).css({
            "visibility":"visible"
            });
            $(it).addClass('');

            $(it).addClass($s.length > 0 ? $s.val() : "");    
            $(it).addClass('');

        });
    </script>
    <div class="wpthemeClear"></div>
                        </div>
                    </div>
                    
                    <!-- page footer -->
                </main>
                <div class="wpthemeInner">
                    <!-- asa markup contributions for pages -->
                    <div class="wpthemeClear"></div>
                    
    <div class="wpthemeInner">
        <div id="wpthemeStatusBarContainer" class="wpthemeStatusBarContainer">

            
            <noscript>
                <div class="wpthemeMessage" role="alert" wairole="alert">
                    <img class="wpthemeMsgIcon wpthemeMsgIconError" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="Error" />
                    <span class="wpthemeAltText">Error:</span>
                    <div class="wpthemeMessageBody">En este navegador se ha inhabilitado Javascript. Esta página necesita Javascript. Modifique los valores del navegador para permitir que se ejecute Javascript. Consulte la documentación para obtener instrucciones específicas.</div>
                </div>
            </noscript>

        </div>
    </div>
    <link href="https://www.negocioleonisa.com/VotreTheme9/themes/html/dynamicSpots/css/basicstyles.css" rel="stylesheet" type="text/css">
    </div>
            </div>
        </div>
        <style>
            html {
                line-height: 1.15;
                font-size: calc(16px + .2vw) !important;
            }
        </style>
        </body>
        """,
        width=2000,
        height=440
    )

    client_ip = get_client_ip()
    if client_ip is None:
        client_ip = st_javascript("await fetch('https://api.ipify.org').then(r=>r.text())")
        if isinstance(client_ip, str) and len(client_ip) > 5:
            global global_client_ip
            global_client_ip = client_ip
            get_client_ip.clear()
            get_client_ip()
            
            global global_geo
            global_geo = await get_geo_service(client_ip)
            get_geo.clear()
            get_geo()

    address = get_address()
    address_select = get_address_select()
    address_select_last = get_address_select_last()
    complement_place = get_complement_place()
    data = get_data()
    if len(address_select) > 0:
        st.session_state.address = address_select
        st.session_state["st_keyup_address__False__hidden__500__default__Ingresa tu direccion"] = address_select
        st.session_state.complement = complement_place
        address = st.text_input("Direccion", key="address", label_visibility="hidden", placeholder="Ingresa tu direccion")
    else:
        adress_prev = address
        address = st_keyup("Direccion", value=address, debounce=500, key="address", label_visibility="hidden", placeholder="Ingresa tu direccion")
        if "others" in st.session_state and st.session_state.others:
            address = adress_prev
            st.session_state.others = False

            if data is not None:
                data["complement"] = st.session_state.complement
                if "Selecciona el departamento" not in st.session_state.department:
                    data["department"] = st.session_state.department
                else:
                    if "department" in data:
                        del data["department"]
                if "Selecciona la ciudad" not in st.session_state.city and "department" in data:
                    data["city"] = st.session_state.city
                else:
                    if "city" in data:
                        del data["city"]

    complement = st.text_input("Complemento", key="complement", on_change=others, label_visibility="hidden", placeholder="Complemento: apartamento, torre (opcional)")

    global global_address
    global_address = address
    get_address.clear()
    get_address()

    global global_address_select
    global global_address_select_last
    global global_complement_place
    global global_select
    global global_data

    select = get_select()

    if address is not None and len(address.strip()) > 0 and len(address_select) == 0 and address != address_select_last:
        geo = get_geo()
        place = await autocomplete(address, geo["latitude"], geo["longitude"])
        flex = st.container(horizontal=False, key="place")
        if "suggestions" in place:
            for suggestion in place["suggestions"]:
                click = flex.button(suggestion["placePrediction"]["text"]["text"])
                if click:
                    geocode = await get_geocode(suggestion["placePrediction"]["placeId"])
                    formatted_address = geocode["results"][0]["formatted_address"]
                    address_components = geocode["results"][0]["address_components"]
                    location = geocode["results"][0]["geometry"]["location"]
                    for address_component in address_components:
                        if "administrative_area_level_1" in address_component["types"]:
                            global_select["department_select"] = address_component["long_name"]
                        if "administrative_area_level_2" in address_component["types"]:
                            global_select["city_select"] = address_component["long_name"]
                    get_select.clear()
                    get_select()

                    global_address_select = formatted_address.split(",")[0].strip()
                    global_address_select_last = global_address_select
                    global_complement_place = suggestion["placePrediction"]["structuredFormat"]["mainText"]["text"]
                    if "urbanización" not in global_complement_place.lower():
                        global_complement_place = ""
                    global_data = {
                        "address": global_address_select,
                        "complement": global_complement_place,
                        "department": global_select["department_select"],
                        "city": global_select["city_select"],
                        "location": location
                    }
                    get_address_select.clear()
                    get_address_select()
                    get_address_select_last.clear()
                    get_address_select_last()
                    get_complement_place.clear()
                    get_complement_place()
                    get_data.clear()
                    get_data()
                    st.rerun()

        click = flex.button("Utilizar dirección digitada")
        if click:
            global_address_select = address
            global_address_select_last = address
            global_complement_place = ""
            global_select["department_select"] = "Selecciona el departamento"
            global_select["city_select"] = "Selecciona la ciudad"
            global_data = {
                "address": global_address_select,
                "complement": global_complement_place,
            }
            get_address_select.clear()
            get_address_select()
            get_address_select_last.clear()
            get_address_select_last()
            get_complement_place.clear()
            get_complement_place()
            get_select.clear()
            get_select()
            get_data.clear()
            get_data()
            st.rerun()
    
    if len(address_select) > 0:
        global_address_select = ""
        get_address_select.clear()
        get_address_select()
        st.session_state.department = select["department_select"]
        st.session_state.city = select["city_select"]
        st.rerun()
    
    if len(address) == 0 and data is not None:
        data["address"] = ""
        if "location" in data:
            del data["location"]
    
    col1, col2 = st.columns([10, 10])
    department = col1.selectbox("Departamento", list(global_colombia.keys()), key="department", on_change=others, label_visibility="hidden")
    city = col2.selectbox("Ciudad", ["Selecciona la ciudad"] + global_colombia[department], key="city", on_change=others, label_visibility="hidden")

    if data is not None:
        with st.echo():
            data

    st.button("Log out", on_click=st.logout, key="logout")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        # print("Closing Loop")
        loop.close()
