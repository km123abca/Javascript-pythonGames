let scenes=[
			[
				// {"sprite":"platform","x":150,"y":-160,"width":50,"height":1280},
				// {"sprite":"WallGripper","x":125,"y":-177,"width":50,"height":1304},
			    {"sprite":"thorn","x":1870,"y":924,"width":600,"height":250,"xoffset":0,"yoffset":0},
			    {"sprite":"shrub","x":200,"y":924,"width":2400,"height":250,"xoffset":0,"yoffset":0},
			    {"sprite":"shrub","x":3675,"y":924,"width":2400,"height":250,"xoffset":0,"yoffset":0},
				{"sprite":"tree","x":-950,"y":424,"width":361,"height":343},
				{"sprite":"platform","x":-150,"y":600,"width":1987,"height":50},
				{"sprite":"platform","x":1459,"y":479,"width":1200,"height":50},
				{"sprite":"platform","x":3228,"y":696,"width":2313,"height":50},				
				{"sprite":"player","x":100,"y":200,"width":100,"height":100},
				{"sprite":"camstopper_left","x":-565,"y":-491},//394
				{"sprite":"camstopper_right","x":3591,"y":582},
				{"sprite":"entryexit_entry","x":-344,"y":464},
				{"sprite":"entryexit_exit","x":4059,"y":610},
				{"sprite":"scenechanger_scright","x":4315,"y":572},
				{"sprite":"MarkedSpot_fkjumpup","x":825,"y":526},
				{"sprite":"MarkedSpot_fkjumpup","x":2112,"y":614},				
				// {"sprite":"huskMiner","x":73,"y":431,"width":170,"height":220,"spriteId":"boss_huskminer1"}
				// {"sprite":"lance","x":300,"y":200,"width":250,"height":200,spriteId:"lance1"},
				{"sprite":"husk","x":1616,"y":300,"width":150,"height":200,"spriteId":"husk1"},
				{"sprite":"flower","x":-69,"y":554,"width":50,"height":50,"xoffset":0,"yoffset":0,"exp":10,"spriteId":"f1"},
				{"sprite":"flower","x":93,"y":554,"width":50,"height":50,"xoffset":0,"yoffset":0,"exp":10,"spriteId":"f2"},
				{"sprite":"flower","x":268,"y":554,"width":50,"height":50,"xoffset":0,"yoffset":0,"exp":10,"spriteId":"f3"},	
				{"sprite":"flower","x":1081,"y":430,"width":50,"height":50,"xoffset":0,"yoffset":0,"exp":10,"spriteId":"f4"},				
			],
            [                               
                {"sprite":"platform","x":-1110,"y":600,"width":775,"height":50},
                {"sprite":"wall","x":-887,"y":2156,"width":250,"height":150,"isHorizontal":false,"copies":5},  
                {"sprite":"wall","x":1888,"y":1698,"width":250,"height":150,"isHorizontal":false,"copies":5},    
                {"sprite":"wall","x":-812,"y":837,"width":250,"height":150,"isHorizontal":false,"copies":6},
                {"sprite":"wall","x":750,"y":462,"width":250,"height":150,"isHorizontal":false,"copies":4},
                {"sprite":"wall","x":-587,"y":612,"width":250,"height":150,"isHorizontal":true,"copies":5},
                {"sprite":"wall","x":-450,"y":1000,"width":250,"height":150,"isHorizontal":true,"copies":5},
                {"sprite":"wall","x":-762,"y":1713,"width":250,"height":150,"isHorizontal":true,"copies":10},  
                {"sprite":"wall","x":-550,"y":2450,"width":250,"height":150,"isHorizontal":true,"copies":10}, 
                {"sprite":"wall","x":-700,"y":2935,"width":250,"height":150,"isHorizontal":true,"copies":15},                     
                {"sprite":"camstopper_left","x":-600,"y":394},
                {"sprite":"camstopper_right","x":1350,"y":2778},
                {"sprite":"entryexit_entry","x":-900,"y":464},
                {"sprite":"entryexit_exit","x":2100,"y":2819},
                {"sprite":"scenechanger_scleft","x":-1450,"y":464},
                {"sprite":"scenechanger_scright","x":2300,"y":2805},
                {"sprite":"BossFightTriggGO","x":0,"y":2111,"mywidth":40,"myheight":600,
				 "br1posx":-660,"br1posy":-147,"br2posx":1600,"br2posy":-147,
				 "spriteId":"BossFightTriggGO"
				}, 
				// {"sprite":"falseknight","x":625,"y":1944,"width":368,"height":223,
				//  "spriteId":"boss_fknight1","spawnedBoss":false},
				{"sprite":"huskMiner","x":550,"y":2260,"width":170,"height":220,
				   "spriteId":"boss_huskminer1","cutscene":true}              
            ],
			[
			  {"sprite":"platform","x":0,"y":600,"width":1987,"height":50},
			  {"sprite":"platform","x":2100,"y":1000,"width":1000,"height":50},
			  {"sprite":"platform","x":2100,"y":1350,"width":1000,"height":50},
			  {"sprite":"thorn","x":1025,"y":507,"width":300,"height":250,"xoffset":0,"yoffset":0},
			  {"sprite":"thorn","x":1762,"y":914,"width":300,"height":250,"xoffset":0,"yoffset":0},
			  {"sprite":"camstopper_left","x":-303,"y":400},
			  {"sprite":"camstopper_right","x":1822,"y":1190},
			  {"sprite":"entryexit_entry","x":-825,"y":400},
			  {"sprite":"entryexit_exit","x":2350,"y":1215},
			  {"sprite":"scenechanger_scleft","x":-970,"y":464},
			  {"sprite":"saw","x":437,"y":416,"width":112,"height":112,"xoffset":0,"yoffset":0,"moveTime":600,"moveTimeInit":200,"speed":10,"isHoriWheel":false},
			  {"sprite":"saw","x":137,"y":175,"width":112,"height":112,"xoffset":0,"yoffset":0,"moveTime":600,"moveTimeInit":600,"speed":10,"isHoriWheel":false},
			  {"sprite":"scenechanger_scright","x":2598,"y":1190},
			],
			[			  
			  {"sprite":"wall","x":-888,"y":612,"width":250,"height":150,"isHorizontal":true,"copies":5},
			  {"sprite":"wall","x":388,"y":868,"width":250,"height":150,"isHorizontal":true,"copies":4},
			  {"sprite":"wall","x":1738,"y":868,"width":250,"height":150,"isHorizontal":true,"copies":4},
			  {"sprite":"wall","x":1300,"y":612,"width":250,"height":150,"isHorizontal":true,"copies":2},
			  {"sprite":"wall","x":2713,"y":868,"width":250,"height":150,"isHorizontal":true,"copies":4},	  
			  {"sprite":"camstopper_left","x":-303,"y":400},
			  {"sprite":"camstopper_right","x":2585,"y":610},
			  {"sprite":"entryexit_entry","x":-825,"y":400},
			  {"sprite":"entryexit_exit","x":3100,"y":710},
			  {"sprite":"scenechanger_scleft","x":-970,"y":464},
			  // {"sprite":"saw","x":800,"y":748,"width":112,"height":112,"xoffset":0,"yoffset":0,
			  // "moveTime":1200,"moveTimeInit":400,"speed":10,"isHoriWheel":true},
			  // {"sprite":"saw","x":2100,"y":748,"width":112,"height":112,"xoffset":0,"yoffset":0,
			  // "moveTime":1200,"moveTimeInit":600,"speed":10,"isHoriWheel":true},
			  // {"sprite":"saw","x":1600,"y":521,"width":112,"height":112,"xoffset":0,"yoffset":0,
			  // "moveTime":2200,"moveTimeInit":0,"speed":3,"isHoriWheel":true},
			  {"sprite":"scenechanger_scright","x":3300,"y":740},

			],
			[
			    // {"sprite":"player","x":200,"y":200,"width":150,"height":100},
			    // {"sprite":"lance","x":1060,"y":200,"width":250,"height":200,spriteId:"lance1"},
			    {"sprite":"husk","x":1062,"y":500,"width":150,"height":200,"spriteId":"husk2"},
			    {"sprite":"thorn","x":-400,"y":824,"width":600,"height":250,"xoffset":0,"yoffset":0},
			    {"sprite":"shrub","x":713,"y":870,"width":1571,"height":217,"xoffset":0,"yoffset":0},
			    {"sprite":"platform","x":-1110,"y":600,"width":775,"height":50},	
				{"sprite":"platform","x":563,"y":600,"width":2200,"height":50},				
				{"sprite":"camstopper_left","x":-600,"y":394},
				{"sprite":"camstopper_right","x":925,"y":447},
				{"sprite":"entryexit_entry","x":-1250,"y":464},
				{"sprite":"entryexit_exit","x":1262,"y":394},
				{"sprite":"scenechanger_scleft","x":-1450,"y":464},
				{"sprite":"scenechanger_scright","x":1637,"y":468},
				{"sprite":"MarkedSpot_enemystopleft","x":280,"y":523}
			],
			[	
			    {"sprite":"shrub","x":-425,"y":994,"width":1111,"height":250,"xoffset":0,"yoffset":0},
			    {"sprite":"shrub","x":1475,"y":994,"width":1312,"height":171,"xoffset":0,"yoffset":0},
			     {"sprite":"shrub","x":3138,"y":994,"width":1312,"height":171,"xoffset":0,"yoffset":0},
			    {"sprite":"thorn","x":400,"y":947,"width":736,"height":250,"xoffset":0,"yoffset":0},
			    {"sprite":"thorn","x":2338,"y":1000,"width":948,"height":250,"xoffset":0,"yoffset":0},		    
				{"sprite":"platform","x":-274,"y":600,"width":1625,"height":50},		
				{"sprite":"platform","x":1350,"y":770,"width":2000,"height":50},	
				{"sprite":"platform","x":3039,"y":600,"width":1500,"height":50},			
				{"sprite":"camstopper_left","x":-282,"y":394},
				{"sprite":"camstopper_right","x":2870,"y":747},
				{"sprite":"entryexit_entry","x":-850,"y":464},
				{"sprite":"entryexit_exit","x":3288,"y":394},
				{"sprite":"scenechanger_scleft","x":-1057,"y":464},
				{"sprite":"scenechanger_scright","x":3500,"y":460},				
				{"sprite":"BossFightTriggGO","x":1824,"y":628,
				 "br1posx":-1100,"br1posy":-60,"br2posx":200,"br2posy":-60,"spriteId":"BossFightTriggGO"
				},
				// {"sprite":"falseknight","x":1289,"y":-367,"width":368,"height":223,"spriteId":"boss_fknight1","spawnedBoss":true}
				// {"sprite":"huskMiner","x":889,"y":-367,"width":170,"height":220,"spriteId":"boss_huskminer1","cutscene":false}
			],
			
			[
			    {"sprite":"shrub","x":-113,"y":932,"width":1362,"height":250,"xoffset":0,"yoffset":0},
			    {"sprite":"shrub","x":450,"y":1256,"width":1171,"height":171,"xoffset":0,"yoffset":0},
			    {"sprite":"thorn","x":1225,"y":1240,"width":903,"height":250,"xoffset":0,"yoffset":0},
			    {"sprite":"shrub","x":4562,"y":1657,"width":1561,"height":171,"xoffset":0,"yoffset":0},
			    {"sprite":"thorn","x":3313,"y":1626,"width":1107,"height":250,"xoffset":0,"yoffset":0},
				{"sprite":"platform","x":200,"y":600,"width":2200,"height":50},		
				{"sprite":"platform","x":2363,"y":1000,"width":2200,"height":50},	
				{"sprite":"platform","x":3576,"y":1179,"width":250,"height":50},
				{"sprite":"platform","x":4576,"y":1370,"width":2200,"height":50},	
				{"sprite":"platform","x":1288,"y":800,"width":250,"height":50},	
				{"sprite":"camstopper_left","x":-115,"y":394},
				{"sprite":"camstopper_right","x":4838,"y":1550},
				{"sprite":"entryexit_entry","x":-457,"y":464},
				{"sprite":"entryexit_exit","x":4950,"y":1252},
				{"sprite":"scenechanger_scleft","x":-794,"y":464},
				// {"sprite":"huskMiner","x":2900,"y":500,"width":170,"height":220,"spriteId":"boss_huskminer1","cutscene":true}
				{"sprite":"scenechanger_scright","x":5650,"y":1208}
			],
			[			    
			    {"sprite":"lance","x":460,"y":1300,"width":250,"height":200,spriteId:"miniboss_lance1"},			    
			    {"sprite":"platform","x":-1110,"y":600,"width":775,"height":50},	
			    {"sprite":"wall","x":750,"y":462,"width":250,"height":150,"isHorizontal":false,"copies":4},
			    {"sprite":"wall","x":-587,"y":612,"width":250,"height":150,"isHorizontal":true,"copies":5},
			    {"sprite":"wall","x":-450,"y":1000,"width":250,"height":150,"isHorizontal":true,"copies":5},
			    {"sprite":"wall","x":-762,"y":1560,"width":250,"height":150,"isHorizontal":true,"copies":10},						
				{"sprite":"camstopper_left","x":-600,"y":394},
				{"sprite":"camstopper_right","x":800,"y":1375},
				{"sprite":"entryexit_entry","x":-900,"y":464},
				{"sprite":"entryexit_exit","x":1262,"y":1375},
				{"sprite":"scenechanger_scleft","x":-1450,"y":464},
				{"sprite":"scenechanger_scright","x":1637,"y":1375},
				{"sprite":"tree","x":937,"y":1300,"width":361,"height":490},
			],
		   ];