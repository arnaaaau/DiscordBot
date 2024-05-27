import json
import os
import random
import signal
import sys

from discord import Intents
from discord.ext import commands, tasks

# Crear un objeto Intents con los intents necesarios
intents = Intents.default()
intents.members = True  # Habilita el intent para recibir eventos de miembros
intents.message_content = True  # Habilita el intent de contenido de mensajes



el_quijote = quijote_paragraphs = [
    "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lentejas los viernes, algún palomino de añadidura los domingos, consumían las tres partes de su hacienda. El resto della concluían sayo de velarte, calzas de velludo para las fiestas, con sus pantuflos de lo mismo, los días de entre semana se honraba con su vellori de lo más fino. Tenía en su casa una ama que pasaba de los cuarenta, y una sobrina que no llegaba a los veinte, y un mozo de campo y plaza, que así ensillaba el rocín como tomaba la podadera. Frisaba la edad de nuestro hidalgo con los cincuenta años; era de complexión recia, seco de carnes, enjuto de rostro; gran madrugador y amigo de la caza. Quieren decir que tenía el sobrenombre de Quijada, o Quesada, que en esto hay alguna diferencia en los autores que deste caso escriben; aunque por conjeturas verosímiles se deja entender que se llama Quijana; pero esto importa poco a nuestro cuento; basta que en la narración dél no se salga un punto de la verdad.",
    "Es, pues, de saber que este sobredicho hidalgo, los ratos que estaba ocioso, que eran los más del año, se daba a leer libros de caballerías con tanta afición y gusto, que olvidó casi de todo punto el ejercicio de la caza, y aún la administración de su hacienda; y llegó a tanto su curiosidad y desatino en esto, que vendió muchas hanegas de tierra de sembradura, para comprar libros de caballerías en que leer; y así llevó a su casa todos cuantos pudo haber dellos; y de todos ningunos le parecían tan bien como los que compuso el famoso Feliciano de Silva: porque la claridad de su prosa y aquellas intrincadas razones suyas le parecían de perlas; y más cuando llegaba a leer aquellos requiebros y cartas de desafíos, donde en muchas partes hallaba escrito: la razón de la sinrazón que a mi razón se hace, de tal manera mi razón enflaquece, que con razón me quejo de la vuestra fermosura, y también cuando leía: los altos cielos que de vuestra divinidad divinamente con las estrellas os fortifican, y os hacen merecedora del merecimiento que merece la vuestra grandeza.",
    "Con estas razones perdía el pobre caballero el juicio, y desvelábase por entenderlas y desentrañarles el sentido, que no se lo sacara, ni las entendiera el mismo Aristóteles, si resucitara para sólo ello. No estaba muy bien con las heridas que don Belianis daba y recibía, porque se imaginaba que por grandes maestros que le hubiesen curado, no dejaría de tener el rostro y todo el cuerpo lleno de cicatrices y señales. Pero con todo alababa en su autor aquel acabar su libro con la promesa de aquella inacabable aventura, y muchas veces le vino deseo de tomar la pluma y darle fin al pie de la letra como allí se promete; y sin duda alguna lo hiciera, y aun saliera con ello, si otros mayores y continuos pensamientos no se lo estorbaran.",
    "Tuvo muchas veces competencia con el cura de su lugar (que era hombre docto, graduado en Sigüenza), sobre cuál había sido mejor caballero, Palmerín de Inglaterra o Amadís de Gaula; mas maese Nicolás, barbero del mismo pueblo, decía que ninguno llegaba al caballero del Febo, y que si alguno se le podía comparar, era don Galaor, hermano de Amadís de Gaula, porque tenía muy acomodada condición para todo; que no era caballero melindroso, ni tan llorón como su hermano, y que en lo de la valentía no le iba en zaga.",
    "En resolución, él se enfrascó tanto en su lectura, que se le pasaban las noches leyendo de claro en claro, y los días de turbio en turbio, y así, del poco dormir y del mucho leer, se le secó el cerebro, de manera que vino a perder el juicio. Llenósele la fantasía de todo aquello que leía en los libros, así de encantamientos, como de pendencias, batallas, desafíos, heridas, requiebros, amores, tormentas y disparates imposibles; y asentósele de tal modo en la imaginación que era verdad toda aquella máquina de aquellas sonadas soñadas invenciones que leía, que para él no había otra historia más cierta en el mundo. Decía él que el Cid Ruy Díaz había sido muy buen caballero, pero que no tenía que ver con el caballero de la Ardiente Espada, que de sólo un revés había partido por medio dos fieros y descomunales gigantes. Mejor estaba con Bernardo del Carpio, porque en Roncesvalles había muerto a Roldán el encantado, valiéndose de la industria de Hércules, cuando ahogó a Anteo, el hijo de la Tierra, entre los brazos. Decía mucho bien del gigante Morgante, porque, con ser de aquella generación gigantea, que todos son soberbios y descomedidos, él solo era afable y bien criado. Pero sobre todos estaba bien con Reinaldos de Montalbán, y más cuando le veía salir de su castillo y robar cuantos topaba, y cuando en allende robó aquel ídolo de Mahoma, que era todo de oro, según dice su historia. Diera él, por dar una mano de coces al traidor de Galalón, al ama que tenía y aún a su sobrina de añadidura.",
    "En efecto, rematado ya su juicio, vino a dar en el más extraño pensamiento que jamás dio loco en el mundo, y fue que le pareció convenible y necesario, así para el aumento de su honra como para el servicio de su república, hacerse caballero andante, e irse por todo el mundo con sus armas y caballo a buscar las aventuras, y a ejercitarse en todo aquello que él había leído que los caballeros andantes se ejercitaban, deshaciendo todo género de agravio, y poniéndose en ocasiones y peligros donde, acabándolos, cobrase eterno nombre y fama. Imaginábase el pobre ya coronado por el valor de su brazo, por lo menos del imperio de Trapisonda; y así, con estos tan agradables pensamientos, llevado del extraño gusto que en ellos sentía, se dio priesa a poner en efeto lo que deseaba.",
    "Y lo primero que hizo fue limpiar unas armas que habían sido de sus bisabuelos, que, tomadas de orín y llenas de moho, luengos siglos había que estaban puestas y olvidadas en un rincón. Púsoles lanzadera y se remendó con cartón y otros artilugios, haciéndoles de nuevo una celada de encaje, que había de peor era celada de bacín. Luego fue a ver su rocín, y aunque tenía más cuartos que un real y más tachas que el caballo de Gonela, que tantum pellis et ossa fuit, parecióle que ni el Bucéfalo de Alejandro, ni Babieca el del Cid, con él se igualaban. Cuatro días se le pasaron en imaginar qué nombre le pondría; porque (según se decía él a sí mismo) no era razón que caballo de caballero tan famoso, y tan bueno él por sí, estuviese sin nombre conocido; y así procuraba acomodársele de modo que declarase quién había sido antes que fuese de caballero andante, y lo que era entonces; pues estaba muy puesto en razón que, mudando su señor estado, mudase él también nombre, y le cobrase famoso y de ruido, como convenía a la nueva orden y al nuevo ejercicio que ya profesaba. Y así, después de muchos nombres que formó, borró y quitó, añadió, deshizo y tornó a hacer en su memoria e imaginación, al fin le vino a llamar Rocinante, nombre, a su parecer, alto, sonoro y significativo de lo que había sido cuando fue rocín, antes de lo que ahora era: que era antes y primero de todos los rocines del mundo.",
    "Puesto nombre y tan a su gusto a su caballo, quiso ponérsele a sí mismo, y en este pensamiento duró otros ocho días, y al cabo se vino a llamar don Quijote; de donde, como queda dicho, tomaron ocasión los autores desta tan verdadera historia que sin duda se debía de llamar Quijada, y no Quesada, como otros quisieron decir. Pero acordándose que el valeroso Amadís no sólo se había contentado con llamarse Amadís a secas, sino que añadió el nombre de su reino y patria, por hacerla famosa, y se llamó Amadís de Gaula, así quiso, como buen caballero, añadir al suyo el nombre de su tierra y llamarse Don Quijote de la Mancha, con que a su parecer declaraba muy al vivo su linaje y patria, y la honraba con tomar el sobrenombre della.",
    "Limpias, pues, sus armas, hecho del morrión celada, puesto nombre a su rocín y confirmándose a sí mismo, se dio a entender que no le faltaba otra cosa sino buscar una dama de quien enamorarse; porque el caballero andante sin amores era árbol sin hojas y sin fruto, y cuerpo sin alma. Decíase él a sí: Si yo, por malos de mis pecados, o por mi buena suerte, me encuentro por ahí con algún gigante, como de ordinario les acontece a los caballeros andantes, y le derribo de un encuentro, o le parto por mitad del cuerpo, o finalmente le venzo y le rindo, ¿no será bien tener a quien enviarle presentado, y que entre y se hinque de rodillas ante mi dulce señora, y diga con voz humilde y rendida: Yo, señora, soy el gigante Caraculiambro, señor de la ínsula Malindrania, a quien venció en singular batalla el jamás como se debe alabado caballero Don Quijote de la Mancha, el cual me mandó que me presentase ante vuestra merced, para que la vuestra grandeza disponga de mí a su talante?",
    "Oh, ¡cómo se holgó nuestro buen caballero cuando hubo hecho este discurso, y más cuando halló a quién dar nombre de su dama! Y fue, a lo que se cree, que en un lugar cerca del suyo había una moza labradora de muy buen parecer, de quien él un tiempo anduvo enamorado, aunque, según se entiende, ella jamás lo supo ni se dio cata dello. Llamábase Aldonza Lorenzo, y a esta le pareció ser bien darle título de señora de sus pensamientos; y, buscándole nombre que no desdijese mucho del suyo, y que tirase y se encaminase al de princesa y gran señora, vino a llamarla Dulcinea del Toboso, porque era natural del Toboso: nombre, a su parecer, músico y peregrino y significativo, como todos los demás que a él y a sus cosas había puesto.",
    "Hechas, pues, estas prevenciones, no quiso aguardar más tiempo a poner en efeto su pensamiento, apretándole a ello la falta que él pensaba que hacía en el mundo su tardanza, según eran los agravios que pensaba deshacer, tuertos que enderezar, sinrazones que emendar, abusos que mejorar, y deudas que satisfacer. Y así, sin dar parte a persona alguna de su intención, y sin que nadie le viese, una mañana, antes del día (que era uno de los calurosos del mes de julio), se armó de todas sus armas, subió sobre Rocinante, puesta su mal compuesta celada, embrazó su adarga, tomó su lanza, y por la puerta falsa de un corral salió al campo con grandísimo contento y alborozo de ver con cuánta facilidad había dado principio a su buen deseo. Mas apenas se vio en el campo, cuando le asaltó un pensamiento terrible, y tal, que por poco le hiciera dejar la comenzada empresa; y fue que le vino a la memoria que no era armado caballero, y que, conforme a la ley de caballería, ni podía ni debía tomar armas con ningún caballero; y puesto que lo fuera, había de llevar armas blancas, como novel caballero, sin empresa en el escudo, hasta que por su esfuerzo la ganase. Estos pensamientos le hicieron titubear en su propósito; mas pudiendo más su locura que otra razón alguna, propuso de hacerse armar caballero del primero que topase, a imitación de otros muchos que así lo hicieron, según él había leído en los libros que tal le tenían.",
    "En lo del armas blancas, pensaba limpiarlas de manera, en teniendo lugar, que lo fuesen más que un arminio. Con esto se quietó y prosiguió su camino, sin llevar otro que aquel que su caballo quería, creyendo que en aquello consistía la fuerza de las aventuras. Yendo, pues, caminando nuestro flamante aventurero, iba hablando consigo mesmo y diciendo: ¿Quién duda sino que en los venideros tiempos, cuando salga a luz la verdadera historia de mis famosos hechos, que el sabio que los escribiere no ponga, cuando llegue a contar esta mi primera salida tan de mañana, desta manera?: Apenas había el rubicundo Apolo tendido por la faz de la ancha y espaciosa tierra las doradas hebras de sus hermosos cabellos, y apenas los pequeños y pintados pajarillos con sus harpadas lenguas habían saludado con dulce y meliflua armonía la venida de la rosada aurora, que, dejando la blanda cama del celoso marido, por las puertas y balcones del manchego horizonte a los mortales se mostraba, cuando el famoso caballero don Quijote de la Mancha, dejando las ociosas plumas, subió sobre su famoso caballo Rocinante y comenzó a caminar por el antiguo y conocido Campo de Montiel. Y era la verdad que por él caminaba. Y añadió diciendo: Dichosa edad y siglo dichoso aquel adonde saldrán a luz las famosas hazañas mías, dignas de entallarse en bronces, esculpirse en mármoles y pintarse en tablas para memoria en lo futuro. Y tú, ¡oh sabio encantador, quienquiera que seas, a quien ha de tocar el ser cronista desta peregrina historia!, ruégote que no te olvides de mi buen Rocinante, compañero eterno mío en todos mis caminos y carreras. Luego volvía diciendo, como si verdaderamente fuera enamorado: ¡Oh princesa Dulcinea, señora deste cautivo corazón! Mucho agravio me habéis fecho en despedirme y reprocharme con el riguroso mandamiento de no parecer ante la vuestra fermosura. Plégaos, señora, de membraros deste vuestro sujeto corazón, que tantas cuitas por vuestro amor padece.",
    "Con estos iba ensartando otros disparates, todos al modo que sus libros le habían enseñado, imitando en cuanto podía su lenguaje. Con esto caminaba tan despacio, y el sol entraba tan apriesa y con tanto ardor, que fuera bastante a derretirle los sesos, si algunos tuviera.",
    "Anduvo casi todo aquel día sin sucederle cosa que de contar fuese, de lo cual se desesperaba, porque quisiera topar luego luego con quien hacer experiencia de lo que en su valor se encerraba. Autores hay que dicen que la primera aventura que le avino fue la del puerto Lápice; otros dicen que la de los molinos de viento; pero lo que yo he podido averiguar en este caso, y lo que he hallado escrito en los anales de la Mancha, es que él anduvo todo aquel día, y al anochecer su rocín y él se hallaron cansados y muertos de hambre, y mirando a todas partes por ver si descubriría algún castillo o alguna majada de pastores donde recogerse y adonde pudiese remediar su mucha hambre y necesidad, vio no lejos del camino por donde iba una venta, que fue como si viera una estrella que, no a los portales, sino a los alcázares de su redención le encaminaba. Diose priesa a caminar, y llegó a ella a tiempo que anochecía.",
    "Estaban acaso a la puerta dos mujeres mozas, destas que llaman del partido, las cuales iban a Sevilla con unos arrieros, que en la venta aquella noche acertaron a hacer jornada. Y como a nuestro aventurero todo cuanto pensaba, veía o imaginaba, le parecía ser hecho y pasar al modo de lo que había leído, luego que vio la venta se le representó que era castillo con sus cuatro torres y chapiteles de luciente plata, sin faltarle su puente levadiza y honda cava, con todos aquellos adherentes que semejantes castillos se pintan. Fuese llegando a la venta, que a él le parecía castillo, y a poco trecho de ella detuvo las riendas a Rocinante, esperando que algún enano se pusiese entre las almenas a dar señal con alguna trompeta de que llegaba caballero al castillo. Pero como vio que se tardaban, y que Rocinante se daba priesa por llegar a la caballeriza, se llegó a la puerta de la venta, y vio a las dos desvergonzadas damas que allí estaban, que a él le parecieron dos hermosas doncellas o graciosas damas que delante de la puerta del castillo se estaban solazando. A esta sazón sucedió acaso que un porquero que andaba recogiendo de unos rastrojos una manada de puercos (que, sin perdón, así se llaman) tocó un cuerno, a cuya señal ellos se recogen, y al instante se le representó a don Quijote lo que deseaba, que era ser algún enano que hacía señal de su venida; y así, con extraño contento, llegó a la venta y a las damas, las cuales, viendo venir un hombre de aquella manera armado y con lanza y adarga, llenas de miedo se iban a entrar en la venta, mas don Quijote, coligiendo por su huida su miedo, alzándose la visera de papelón y descubriendo su seco y polvoroso rostro, con gentil talante y voz reposada les dijo: No fuyan las vuestras mercedes, ni teman desaguisado alguno, porque a la orden de caballería que profeso no toca ni atañe hacerle a nadie, y menos a tan altas doncellas como vuestras presencias demuestran.",
    "Mirábanle las mozas, y andaban con los ojos buscándole el rostro, que la mala visera le encubría; mas como se oyeron llamar doncellas, cosa tan fuera de su profesión, no pudieron tener la risa, y fue de manera, que don Quijote vino a correrse y a decirles: Bien parece la mesura en las fermosas, y es mucha sandez y desenvoltura la risa que de leve causa procede; pero no os lo digo porque os acuitéis ni mostréis mal talante, que el mío no es otro sino serviros.",
    "El lenguaje no entendido de las señoras, y el mal talle de nuestro caballero acrecentaba en ellas la risa y en él el enojo, y pasara adelante, si a tal hora no saliera el ventero, hombre que, por ser muy gordo, era muy pacífico, el cual, viendo aquella figura contrahecha, armada de armas tan desiguales, como fueron la brida, lanza, adarga y coselete, no estuvo en nada en acompañar a las doncellas en las muestras de su contento. Pero en efeto, temiendo la máquina de tantos pertrechos, determinó hablarle comedidamente, y así le dijo: Si vuestra merced, señor caballero, busca posada, a toda excepción de cama, porque en ella ninguna hay en esta venta, todo lo demás se hallará en mucha abundancia.",
    "Viendo don Quijote la humildad del alcaide de la fortaleza (que tal le pareció a él el ventero y la venta), respondió: Para mí, señor castellano, cualquiera cosa basta, porque mis arreos son las armas, mi descanso el pelear, etcétera."
]

# Crear una instancia del bot con intents
bot = commands.Bot(command_prefix='!', intents=intents)
position = 0

# Registrar una función para manejar la señal SIGINT (Ctrl+C)
def handle_sigint(sig, frame):
    print("Ctrl+C detectado. Guardando datos antes de salir...")
    save_data()
    sys.exit(0)

# Registrar el manejador de señales para SIGINT
signal.signal(signal.SIGINT, handle_sigint)

def load_data():
    global position
    try:
        with open("/home/runner/DiscordBot/data.json", "r") as file:
            data = json.load(file)
            position = data.get('position', 0)
    except FileNotFoundError:
        print("No se encontró el archivo JSON. Creando uno nuevo.")
        position = 0


def save_data():
    data = {'position': position}  # Guardar la posición en un diccionario
    with open("/home/runner/DiscordBot/data.json", "w") as file:
        json.dump(data, file)


@bot.event
async def on_ready():
    print(f'Bot {bot.user} conectado exitosamente.')
    load_data()
    send_quijote_paragraph.start()  # Iniciar la tarea periódica1


@bot.event
async def on_shutdown():
    print("Desconexión del bot. Guardando datos...")
    save_data()


@bot.event
async def on_message(message):
    # Ignorar mensajes enviados por el propio bot
    if message.author == bot.user:
        return

    # Obtener el nombre del autor del mensaje
    author_name = message.author.name
    if author_name == "niiil6322":
        await message.channel.send("ya esta mister datitos dando por culo")
    elif author_name == "adria1003":
        await message.channel.send("el niño de mamá ya llora...")

    if message.content.startswith('!whoami'):
        response = 'Soy como frodo, un simple esclavo de mi señor.'
        await message.channel.send(response)

    # Procesar comandos para que el bot reconozca otros comandos definidos
    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # El usuario se ha unido a un canal de voz
        channel = after.channel  # Definir el canal aquí
        if member.name == "ferrroonn":
            await channel.send('Preparado para servirle, mi señor.')
        else:
            number = random.randint(0, len(frases_vacilonas) - 1)
            await channel.send(frases_vacilonas[number].format(member=member))


@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'¡Bienvenido/a {member.mention} al servidor {guild.name}!'
        await guild.system_channel.send(to_send)


# Definir un comando de ejemplo
@bot.command()
async def saludar(ctx):
    await ctx.send(f'Hola, {ctx.author.name}!')


# Tarea periódica para enviar un párrafo de "El Quijote" cada 24 horas
@tasks.loop(hours=24)
async def send_quijote_paragraph():
    global position
    print('Listo para leer el quijote.')
    channel = bot.get_channel(
        1244664167118671934
    )  # Reemplaza con el ID del canal donde quieres enviar los mensajes
    if channel:
        paragraph = el_quijote[position]
        await channel.send(paragraph)
        position += 1
        if position >= len(el_quijote):
            position = 0


# Ejecutar el bot
bot.run(os.environ['TOKEN'])
