// script obtenu de http://triaslama.wordpress.com/2008/04/01/dynamic-dropdownlist-just-fill-it-with-array/
// please add your city if not added, then go to latlong.py to add their lat-long using google maps or google earth or open street maps
var arr;
var option;

function srcChange(val) {
	var slc_target = document.getElementById("commune");

	switch (val) {
		case "1":
			arr = new Array("Adrar", "Charouine", "Reggane", "Tit", "Timimoun", "Tamantit", "Akabli", "Aougrout", "Bordj Badji Mokhtar");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "2":
			arr = new Array("Boukadir", "Bouzeghaia", "Chlef", "Oued Fodda", "Ouled Fares", "Tenes", "Zeboudja");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "3":
			arr = new Array("Ksar El Hirane", "Hassi Delaa", "Hassi RMel", "Ain Madhi", "Tadjemout", "Brida", "Taouila", "Tadjrouna", "Aflou");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "4":
			arr = new Array("Oum el Bouaghi", "Ain Beida", "Ain Mlila", "Ksar Sbahi", "Ain Fakroun");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "5":
			arr = new Array("Batna", "NGaous", "Ain Yagout", "Seggana", "Barika", "Ain Touta", "Timgad");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "6":
			arr = new Array("Bejaia", "Souk El Tenine", "Tichy", "Akbou", "Tazmalt", "SidiAich", "El Kseur", "Kherrata");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "7":
			arr = new Array("Ain Naga", "Biskra", "Ouled Djellal", "Ourlal", "Sidi Khaled", "Sidi Okba", "Tolga");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "8":
			arr = new Array("Bechar", "Meridja", "Beni Abbes", "Mechraa Houari Boumedienne", "Kenadsa", "Igli", "Tabelbala", "Taghit", "El Ouata", "Kerzaz", "Tamtert", "Beni Ounif");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "9":
			arr = new Array("Blida", "Chrea", "El Affroun", "Boufarik", "Larbaa");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "10":
			arr = new Array("Ain Bessem", "Bir Ghbalou", "Bouira", "Dirrah", "El Asnam", "Lakhdaria", "MChedallah", "Sour El Ghouzlane");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "11":
			arr = new Array("Tamanrasset", "Abalessa", "In Ghar", "In Guezzam", "In Salah", "In Amguel");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "12":
			arr = new Array("Tebessa", "Bir elAter", "Cheria", "El Aouinet", "Negrine", "Morsott", "El Ogla", "Bekkaria", "Ouenza", "Ferkane");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "13":
			arr = new Array("Tlemcen", "Remchi", "Sabra", "Ghazaouet", "Ouled Mimoun", "Bab El Assa", "Bensekrane", "Maghnia", "Hammam Boughrara", "Sebdou");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "14":
			arr = new Array("Ain Deheb", "Ain Kermes", "Dahmouni", "Frenda", "Ksar Chellala", "Mahdia", "Rahouia", "Sougueur", "Tiaret");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "15":
			arr = new Array("Tizi Ouzou", "Ain El Hammam", "Freha", "Mechtras", "Draa El Mizan", "Ierhounene", "Azazga", "Yakouren", "Beni Douala", "Bouzguen", "Ouadhia", "Azeffoun", "Tigzirt", "Boghni", "Ifigha", "Tirmitine", "Beni Ziki", "Draa Ben Khedda", "Idjeur", "Mekla", "Beni Yenni", "Tadmait");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "16":
			arr = new Array("Alger", "Dar El Beida", "Reghaia", "Staoueli");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "17":
			arr = new Array("Ain Oussara", "Benhar", "Birine", "Djelfa", "Hassi Bahbah", "Messad");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "18":
			arr = new Array("Jijel", "El Aouana", "Ziama Mansouriah", "Taher", "El Milia", "El Ancer");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "19":
			arr = new Array("Ain Arnat", "Ain Azel", "Ain Lahdjar", "Ain Oulmene", "Belaa", "Djemila", "El Eulma", "Hammam Soukhna", "Mezloug", "Salah Bey", "Setif", "Tizi NBechar");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "20":
			arr = new Array("Ain El Hadjar", "Ain Sekhouna", "Ain Soltane", "Moulay Larbi", "Saida", "Sidi Amar", "Sidi Boubekeur");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "21":
			arr = new Array("Ain Bouziane", "Ain Charchar", "Ain Kechra", "Azzaba", "Collo", "El Harrouch", "Salah Bouchaour", "Sidi Mezghiche", "Skikda", "Tamalous");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "22":
			arr = new Array("Marhoum", "Ras El Ma", "Sfisef", "Sidi Ali Boussidi", "Sidi Bel Abbes");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "23":
			arr = new Array("Annaba", "El Hadjar", "Ain Berda");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "24":
			arr = new Array("Guelma", "Heliopolis", "Nechmaya", "Oued Zenati", "Ras El Agba", "Tamlouka");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "25":
			arr = new Array("Ain Abid", "Constantine", "El Khroub", "Ibn Ziad", "Zighoud Youcef");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "26":
			arr = new Array("Ain Boucif", "Berrouaghia", "Boughezoul", "Bouskene", "Chahbounia", "El Azizia", "El Omaria", "Ksar Boukhari", "Medea", "Tablat");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "27":
			arr = new Array("Ain Boudinar", "Bouguirat", "Fornaka", "Mostaganem", "Oued El Kheir", "Sidi Ali", "Sidi Lakhdar");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "28":
			arr = new Array("Ain El Hadjel", "Ain El Melh", "BouSaada", "Magra", "MSila", "Ouled Derradj", "Sidi Aissa", "Slim", "Tarmount");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "29":
			arr = new Array("Mascara", "Mohammadia", "Oued El Abtal", "Oued Taria", "Sig", "Tighennif");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "30":
			arr = new Array("Hassi Ben Abdellah", "Hassi Messaoud", "NGoussa", "Ouargla", "Touggourt");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "31":
			arr = new Array("Oran", "Gdyel", "Es Senia", "Arzew", "Tafraoui", "BouSfer", "Misserghin", "Boutlelis");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "32":
			arr = new Array("El Bayadh", "Brezina", "Ghassoul", "El Abiodh Sidi Cheikh", "Chellala", "Kraakda", "Tousmouline");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "33":
			arr = new Array("Djanet", "Illizi", "In Amenas");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "34":
			arr = new Array("Ain Taghrout", "Ain Tesra", "Bordj Bou Arreridj", "El Achir", "El Anasser", "El Hamadia", "El Mhir", "Mansoura", "Ras El Oued", "Sidi Embarek", "Tixter");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "35":
			arr = new Array("Bordj Menaiel", "Boudouaou", "Boumerdes", "Dellys", "Issers", "Naciria", "Thenia", "Zemmouri");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "36":
			arr = new Array("Ain Kerma", "Ben Mehidi", "Besbes", "Drean", "El Kala", "El Tarf");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "37":
			arr = new Array("Tindouf");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "38":
			arr = new Array("Boucaid", "Bordj Bou Naama", "Khemisti", "Lardjem", "Layoune", "Sidi Abed", "Theniet El Had", "Tissemsilt");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "39":
			arr = new Array("El Oued", "Guemar", "Hassi Khalifa", "Djamaa");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "40":
			arr = new Array("Babar", "Baghai", "Djellal", "Fais", "Kais", "Khenchela", "Tamza");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "41":
			arr = new Array("Souk Ahras", "Sedrata", "Tiffech", "Zaarouria", "Taoura", "Mdaourouch", "Sidi Fredj");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "42":
			arr = new Array("Tipaza", "Hadjout", "Gouraya", "Cherchell", "Bou Ismail", "Kolea");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "43":
			arr = new Array("Chelghoum Laid", "Grarem", "Mila", "Oued Athmania", "Tadjenanet", "Chelghoum Laid");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "44":
			arr = new Array("Ain Benian", "Ain Defla", "El Abadia", "El Attaf", "Khemis Miliana", "Miliana");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "45":
			arr = new Array("Ain Ben Khelil", "Ain Sefra", "Kasdir", "Makman Ben Amer", "Mecheria", "Naama", "Sfissifa", "Tiout");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "46":
			arr = new Array("Ain Temouchent", "Beni Saf", "El Amria");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "47":
			arr = new Array("Berriane", "El Guerrara", "El Golea", "Ghardaia", "Sebseb", "Zelfana");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		case "48":
			arr = new Array("Ammi Moussa", "Mendes", "Merdja Sidi Abed", "Oued Rhiou", "Relizane", "Sidi Khettab", "Sidi MHamed Ben Ali", "Yellel");
			slc_target.disabled = false;
			for (var i = 0; i < arr.length; i++) {
				option = new Option(arr[i], arr[i]);
				slc_target.options[i] = option;
			}
			break;

		default:
			slc_target.disabled = false;
			slc_target.options.length = 0;
			break;
	}
}