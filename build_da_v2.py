#!/usr/bin/env python3
"""Builds aerial duel data v3 (per-player locs) and patches index.html."""
import json, re

# ─────────────────────────────────────────────────────────────────────────────
# Raw player-attributed locs.  Format: "Name|x10,y10,won,j;..."  per line
# ─────────────────────────────────────────────────────────────────────────────
PD923 = (
"Borja Valle Balonga|460,20,0,34;380,380,0,34;1120,510,0,34;1120,340,0,34;1040,400,0,10;500,230,0,10;630,130,0,10;850,360,0,10;670,660,0,10;820,440,0,23;880,140,0,23;830,140,0,28;780,540,0,31;130,310,0,31;1160,440,0,5;730,730,0,5;1130,410,0,22;790,400,0,22;80,490,1,13;750,280,0,13;550,40,0,13;1130,400,0,32;620,110,0,32;630,190,0,32;610,410,0,32;480,650,0,32;160,490,1,21;590,410,0,21;670,360,0,21;720,250,0,21;700,380,0,21;900,310,0,21;670,180,0,26;850,400,0,26;730,390,0,12;560,720,0,12;540,720,0,12;1130,410,0,12;550,470,0,12;810,400,0,4;930,80,0,4;1140,290,0,4;650,250,0,1;710,170,0,1;870,380,0,19;80,320,1,18;640,540,0,8;630,520,0,8;990,540,0,6;960,190,0,6;780,320,0,6;960,570,0,6;970,210,0,25;580,230,0,24;800,90,0,24;690,300,0,24;760,240,0,24;990,140,0,35;790,310,0,35;640,70,0,35;80,450,0,35;490,200,0,27;1100,470,0,27;520,50,0,9;690,300,0,9;890,260,0,9;1000,170,0,9;510,480,0,7;540,160,0,11;"
"670,270,0,11;650,260,0,11;850,120,0,11;530,530,0,11;800,330,0,11;570,190,0,11;290,540,0,11;860,240,0,2;680,260,0,2;640,280,0,2;520,30,0,2;460,40,0,33;720,410,0,33;180,350,0,33;730,240,0,33;920,200,0,33;120,460,0,33;850,170,0,3;680,170,0,3;740,40,0,3;750,220,0,3;640,130,0,3;910,530,0,3;560,660,0,38;750,210,0,38;910,560,0,38\n"
"Germán Novoa Enríquez|200,20,0,34;550,770,0,10;70,450,0,10;60,460,0,10;160,690,0,10;440,640,1,10;80,390,0,23;400,220,0,23;140,60,0,28;310,140,0,28;290,120,0,31;470,520,0,37;140,450,0,37;540,200,0,22;400,420,0,32;430,220,0,32;50,370,1,21;630,370,0,21;200,350,1,21;610,750,0,12;590,260,0,16;470,310,0,16;400,120,0,4;550,360,1,4;550,280,0,29;90,490,1,29;310,560,1,1;120,400,0,18;70,450,0,18;520,190,0,18;80,390,1,18;220,550,0,8;270,520,0,8;540,250,0,20;670,80,1,24;520,260,1,24;1130,370,0,24;110,470,1,24;650,160,0,24;320,300,0,24;120,340,1,24;600,390,0,36;130,230,0,36;460,340,1,36;500,70,0,35;30,390,1,35;280,210,0,35;150,270,1,35;70,370,0,35;80,460,0,35;50,420,1,35;90,310,1,35;480,450,1,27;110,420,1,27;90,450,0,9;110,300,1,17;530,180,0,17;30,330,1,17;40,290,0,17;1080,330,0,15;400,180,0,15;190,410,0,7;100,460,1,7;390,530,0,7;720,600,0,7;160,420,1,7;130,480,0,11;120,460,0,11;1130,440,0,2;330,420,0,2;410,450,1,2;420,650,0,2;110,480,0,2;620,330,0,30;230,290,1,33;630,370,0,33;100,330,1,33;90,420,0,14;690,580,0,3\n"
"Josep Miguel Fernández Codina|1000,650,0,10;1100,510,0,10;670,460,0,10;450,550,0,23;690,180,0,23;560,510,0,28;860,130,0,28;720,310,0,28;900,700,0,37;760,390,0,5;730,790,0,5;700,710,0,5;1010,730,0,22;1160,200,0,22;940,540,0,22;900,290,0,22;1150,360,0,22;860,590,0,22;1100,500,0,13;730,490,0,32;800,530,0,32;1040,570,0,32;80,460,0,21;1030,420,0,21;870,520,0,12;580,430,0,16;520,530,1,16;1100,390,0,16;1120,460,0,4;730,500,0,29;710,560,0,29;1070,380,0,1;900,200,0,19;1110,210,0,18;1140,250,0,8;850,320,0,8;760,260,0,8;890,270,0,8;410,330,0,6;530,520,0,6;930,180,0,25;670,620,0,24;660,510,0,24;660,420,0,24;870,70,0,24;720,430,0,24;410,110,0,24;670,650,0,36;730,250,0,36;990,560,0,35;710,90,0,27;1100,420,0,27;710,280,0,27;680,240,0,9;640,90,0,9;1020,250,0,9;830,510,0,17;900,510,0,17;580,90,0,7;1090,450,0,7;1100,340,0,7;730,60,0,11;570,140,0,11;580,230,0,11;810,130,0,11;1020,240,0,11;650,550,0,2;960,560,0,30;580,270,0,30;1160,450,0,30;1000,440,0,30;830,490,0,30;910,300,0,30;760,170,0,14;680,120,0,14;630,290,0,14;1140,250,0,14;410,60,0,14;790,190,0,14\n"
"Eneko Undabarrena Ubillos|410,700,0,34;50,390,1,34;480,440,0,10;690,590,0,10;70,420,0,23;520,540,0,28;110,580,0,31;1090,530,0,31;100,420,1,31;80,450,0,31;590,480,1,37;100,390,1,37;380,480,0,37;120,520,1,37;750,770,0,37;80,490,0,37;1150,420,0,37;380,320,1,37;250,330,1,37;470,130,1,5;40,330,1,5;120,470,1,22;50,460,1,32;270,360,0,32;300,580,0,32;770,690,0,12;570,380,0,12;500,490,0,12;770,240,0,12;120,330,1,4;440,200,1,4;410,500,1,4;300,350,1,29;690,320,0,1;520,240,1,1;270,270,1,19;540,170,1,19;1130,580,0,8;670,390,0,8;220,590,0,8;720,630,0,20;470,610,1,20;1100,560,0,20;630,390,0,20;570,590,0,20;320,630,1,25;530,540,0,25;50,460,1,25;260,530,1,24;550,640,0,24;720,270,0,24;570,440,0,24;510,530,0,36;120,380,1,36;450,480,0,36;540,370,1,36;80,360,1,36;470,390,0,35;90,450,0,35;280,320,1,35;80,550,1,9;60,440,1,9;70,540,1,9;840,660,0,15;600,230,0,7;230,370,1,7;550,490,0,7;1000,640,1,11;540,310,0,11;360,300,1,2;110,640,1,30;70,480,0,30;840,730,0,38;460,550,0,38;110,570,1,38\n"
"José Luis Cortés Sen|480,440,0,34;1120,470,0,10;730,530,0,10;950,280,0,23;790,320,0,5;950,110,0,5;570,160,0,5;400,740,0,5;410,230,0,22;570,740,0,22;1160,360,0,32;200,390,0,21;920,340,0,21;660,670,0,21;1150,360,0,21;860,230,0,21;910,530,0,26;490,160,0,12;730,420,0,12;1060,670,0,16;710,280,0,16;1070,380,0,4;660,280,0,4;900,570,0,4;1110,450,0,4;720,670,0,29;810,590,0,29;410,420,0,29;730,140,0,29;790,360,0,1;570,630,0,18;910,200,0,8;880,660,0,8;700,340,0,8;860,460,0,6;670,590,0,6;660,500,0,6;910,620,0,6;320,130,0,6;650,500,0,20;570,610,0,20;700,320,0,20;850,660,0,25;860,430,0,25;1070,440,0,25;660,40,0,25;750,580,0,24;1120,20,0,24;1020,380,0,24;820,320,0,24;740,30,0,36;850,130,0,35;310,760,0,27;820,370,0,9;700,340,0,9;840,600,0,9;720,60,0,9;210,490,0,15;880,360,0,15;720,540,0,7;530,110,0,7;1060,350,0,7;580,430,0,11;750,250,0,11;560,40,0,2;560,730,0,2;1140,370,0,2;1040,420,0,2;640,480,0,30;560,520,0,30;650,630,0,14;730,210,0,14;780,570,0,3;840,390,0,3\n"
"Pau Ferrer Besalduch|740,190,0,10;540,610,0,10;770,440,0,31;1160,470,0,37;790,350,0,5;1150,490,0,5;890,440,0,32;670,380,0,21;710,550,0,26;1160,360,0,16;710,330,0,4;810,390,0,4;630,590,0,4;60,410,1,1;650,360,0,1;830,110,0,19;620,760,0,19;810,450,0,18;140,300,0,18;960,330,0,18;980,180,0,18;750,710,0,18;1130,340,0,8;560,380,0,8;670,280,0,20;720,60,0,20;1110,390,0,20;880,430,0,36;240,220,1,35;930,600,0,35;710,280,0,35;810,390,0,35;1150,380,0,35;1080,310,0,27;790,470,0,9;630,40,0,9;900,270,0,9;760,520,0,9;940,230,0,9;870,670,0,17;780,520,0,15;450,430,0,15;1170,520,0,15;1080,500,0,15;560,110,0,15;840,400,0,7;690,560,0,7;710,580,0,7;70,330,1,7;330,440,0,7;580,300,0,7;1130,440,0,2;790,510,0,2;680,390,0,30;720,390,0,30;610,450,0,33;760,140,0,33;90,500,0,33;710,320,0,33\n"
"Borja Vázquez  Doña|660,660,0,34;900,700,0,23;730,60,0,31;890,390,0,31;790,600,0,31;1030,470,0,37;940,520,0,37;260,260,0,22;700,150,0,22;710,180,0,32;930,290,0,32;1070,490,0,26;940,350,0,12;510,520,0,16;690,220,0,1;880,670,0,1;380,410,0,1;430,500,1,19;470,410,0,8;590,360,0,6;780,220,0,6;1080,480,0,6;410,570,0,25;570,640,0,25;740,760,0,25;610,260,0,25;540,110,0,25;790,550,0,24;780,110,0,36;480,150,0,36;550,60,0,36;830,500,0,35;620,690,0,27;980,490,0,27;460,590,0,27;700,680,0,27;630,460,0,27;580,520,0,27;920,750,0,9;310,430,0,9;640,600,0,17;1050,420,0,11;670,300,0,11;1180,290,0,2;780,240,0,2;30,480,1,2;560,110,0,2;40,410,1,33;710,730,0,33;860,510,0,33;430,60,0,33;490,640,0,14;1070,510,0,14;730,280,0,38;660,330,0,38\n"
"Andoni López Saratxo|270,130,0,34;590,150,0,10;270,180,1,31;80,350,1,31;370,80,1,37;40,240,1,37;180,200,1,37;570,130,0,13;220,50,0,13;60,350,1,13;470,30,1,13;50,550,0,32;500,40,0,32;320,40,1,12;40,580,0,4;30,540,1,4;500,250,1,4;510,230,0,29;210,260,1,1;430,170,0,1;770,120,1,19;90,420,0,19;30,240,0,18;720,70,0,8;610,60,0,20;60,390,1,20;70,240,0,20;430,30,0,25;310,50,1,25;380,140,1,25;290,150,0,25;90,280,0,24;50,420,1,24;750,140,0,27;550,100,1,27;800,70,0,9;610,10,0,9;820,40,0,9;100,360,0,7;350,210,0,11;310,140,1,11;570,230,0,2;680,40,0,30;580,100,0,30;640,130,0,33;490,190,1,33;520,180,0,33;520,270,0,33;100,220,1,33;90,410,0,33;630,140,0,33;640,90,1,14;1060,390,0,14;750,460,0,38\n"
"Abdoulaye Keita Keita|880,360,0,34;580,460,0,34;170,360,1,34;1010,620,0,34;710,120,0,31;840,550,0,37;1170,420,0,37;1170,460,0,37;840,170,0,37;870,630,0,26;770,650,0,4;330,520,0,4;670,110,0,4;830,660,0,29;610,550,0,29;940,520,0,29;570,390,1,29;820,140,0,29;930,630,0,29;810,440,0,1;1000,490,0,1;890,640,0,19;1060,540,0,18;1130,380,0,6;1010,400,0,20;720,200,0,25;810,700,0,24;1000,490,0,24;800,630,0,24;910,500,0,36;690,590,0,36;790,270,0,35;200,560,0,35;530,140,0,35;770,660,0,9;710,540,0,9;390,610,0,15;410,590,0,15;350,560,0,15;890,270,0,7;870,300,0,7;1140,440,0,2;640,710,0,2;720,520,0,38;560,470,0,38;1160,300,0,38\n"
"David Andújar Jiménez|180,280,1,10;140,440,1,10;550,710,0,10;270,480,1,10;350,730,1,5;380,770,1,5;1140,300,0,5;350,780,1,5;90,370,0,22;120,360,0,13;600,630,0,12;80,350,1,12;490,560,0,4;1120,310,0,18;1130,400,0,18;40,380,1,18;810,290,0,18;1030,350,0,18;90,360,1,8;190,480,0,8;100,350,0,36;350,700,1,36;70,370,0,9;350,550,0,9;90,390,1,9;80,400,0,17;440,110,0,7;1150,440,0,7;270,600,1,7;1130,430,0,7;460,190,0,11;110,390,1,11;160,370,0,11;160,560,1,11;40,600,1,11;90,450,1,11;100,500,1,11;540,470,0,33;100,430,1,33;110,340,1,33;340,400,0,33;1090,230,0,14;1090,550,0,14;80,430,1,14;1040,450,0,3\n"
"Boris Sébastien Moltenis|1050,290,0,34;390,180,0,13;70,310,0,21;340,270,1,21;110,430,1,21;630,480,0,21;380,370,0,12;1110,350,0,16;430,350,0,16;110,470,1,16;1130,400,0,16;110,410,0,1;310,310,0,1;360,540,0,19;70,430,0,19;450,220,1,8;120,330,1,8;120,330,0,9;90,360,1,9;370,530,1,17;460,350,0,15;50,430,1,15;1120,530,0,15;600,490,0,15;90,360,0,7;1080,350,0,7;70,460,0,11;170,320,0,11;1140,450,0,2;500,120,1,2;370,200,1,2;460,420,0,2;1010,380,0,2;1180,460,0,14;510,160,0,14;340,230,0,3\n"
"Eugene Adjei Frimpong|420,310,0,10;1170,440,0,28;560,280,0,31;640,360,0,31;230,350,1,13;460,480,0,32;500,200,0,32;140,350,0,32;410,130,0,29;180,140,0,29;670,550,0,25;640,390,0,25;550,280,0,24;590,540,0,24;510,610,1,36;430,400,0,35;640,200,0,27;750,230,0,27;500,210,0,27;380,110,1,9;350,200,0,17;120,400,0,17;130,360,0,17;330,630,1,15;400,490,0,15;990,80,1,7;350,420,0,7;1140,400,0,2;180,150,0,2;390,340,0,33;690,340,0,33;420,400,0,33;680,250,0,14;820,720,0,14;830,170,0,38\n"
"Borislav Ivaylov Stankov|510,530,0,28;1130,390,0,31;790,710,0,31;870,540,0,31;1060,440,0,37;680,430,0,32;640,450,0,32;770,180,0,32;1060,410,0,32;730,730,0,32;1030,450,0,32;1020,550,0,26;1050,440,0,26;830,500,0,26;720,490,0,29;950,640,0,29;580,230,0,29;130,400,0,29;680,90,0,29;810,610,0,29;710,520,0,25;710,160,0,25;940,580,0,24;280,310,0,24;1100,470,0,35;320,510,0,35;570,570,0,27;820,520,0,30;980,530,0,30;1070,460,0,30;160,260,0,30;1090,430,0,30;1060,580,0,33;1050,590,0,38\n"
"Carlos Calderón López|200,450,0,34;1040,610,0,23;970,580,0,23;870,710,0,28;570,610,0,28;1030,710,0,28;670,680,0,31;80,430,1,31;240,360,0,31;760,710,0,37;700,620,0,37;780,690,0,32;920,590,0,29;50,450,0,29;840,730,0,25;880,730,0,25;1000,670,0,36;40,400,0,36;990,720,0,35;1000,720,0,35;90,460,0,35;1120,380,0,33;1170,410,0,33;70,590,1,33;920,740,0,38;720,690,0,38;840,580,0,38\n"
"Jorge Iglesias González|350,590,0,31;1140,530,0,31;670,770,0,37;140,550,1,37;730,670,0,37;450,640,1,37;720,770,0,37;730,760,1,37;830,770,0,37;730,790,0,22;100,420,0,22;100,610,1,22;30,430,0,29;100,410,1,25;80,380,1,25;320,780,0,25;100,440,1,25;290,550,0,25;410,760,1,24;420,700,0,36;130,550,1,36;1120,350,0,35;510,710,1,27;380,760,0,30;240,740,0,30;250,620,0,30\n"
"Eneko Aguilar Elizalde|520,240,0,10;600,630,0,10;880,520,0,12;630,330,0,12;580,590,1,16;1000,330,0,16;360,690,0,16;410,630,0,16;450,290,0,16;570,350,0,4;790,390,0,15;320,600,0,15;110,400,0,15;80,400,0,15;400,300,0,11;390,230,0,11;850,130,0,2;250,170,0,2;1130,350,0,2;450,160,0,14;370,670,0,3;370,590,0,3;910,220,0,3;420,740,0,3\n"
"Mario Jorrín González|120,450,0,34;1140,420,0,34;600,730,0,10;140,610,0,28;360,660,1,28;900,490,0,32;1120,280,0,29;330,550,1,19;80,480,0,18;160,390,0,20;150,580,1,20;500,530,0,35;860,510,0,35;420,420,0,27;1080,310,0,27;1110,380,0,27;360,720,0,27;910,420,0,9;130,390,0,11;660,770,1,33;360,590,0,33\n"
"Federico San Emeterio Díaz|520,700,0,37;340,630,0,5;1110,470,0,21;390,280,0,16;150,270,1,4;710,350,0,1;710,550,1,19;610,460,0,18;590,410,0,18;500,440,0,18;740,280,0,20;260,410,0,9;630,770,1,17;410,580,0,17;690,700,0,7;690,280,0,11;720,150,0,11;910,570,0,11;210,450,0,3\n"
"Vicente Esquerdo Santas|410,300,1,23;1050,550,0,28;90,330,1,31;490,600,1,37;60,530,0,37;1170,330,0,32;780,670,0,32;670,680,0,32;340,610,0,25;560,280,0,24;360,470,0,36;600,330,0,35;360,370,0,35;70,410,1,35;90,320,0,35;700,510,0,33;880,490,0,33;160,230,0,33\n"
"Diego Moreno Garbayo|340,550,0,5;40,510,1,13;580,560,0,16;90,520,1,4;60,410,0,4;640,750,0,18;440,750,0,8;470,780,0,8;220,720,1,8;530,690,0,8;50,500,0,9;710,770,0,17;750,780,0,17;50,580,1,17;590,440,1,17;40,530,1,15;280,610,1,15;960,490,0,14\n"
"Stivan Petkov|1030,150,0,23;860,260,0,23;750,230,0,23;790,270,0,22;790,120,0,22;900,650,0,22\n"
"Vasco Pereira de Sousa|160,220,1,28;100,370,0,16;790,70,0,16;350,290,1,8;70,460,0,35\n"
"Vladyslav Kysil|1060,540,0,28;80,460,1,21;520,370,0,21;1180,470,0,26\n"
"Sergio Benito Crujera|1170,410,0,16;910,210,0,17;1080,440,0,11\n"
"Alejandro Miguel Mula Sanchez|470,560,0,14;1080,320,0,14\n"
"Erik Morán Arribas|730,530,0,22"
)

PD8733 = (
"Pablo González Meixús|440,230,0,24;360,390,0,24;40,580,0,23;350,550,1,23;330,490,1,7;1100,300,0,7;110,380,0,7;460,380,1,9;460,490,0,9;450,520,0,9;280,520,0,9;1080,330,0,34;160,260,1,1;110,470,1,1;500,380,0,13;520,460,0,13;210,460,0,13;160,330,0,3;80,460,0,3;120,370,0,18;440,240,1,18;960,230,0,18;1120,420,0,18;680,70,0,36;480,370,1,35;120,420,0,35;100,330,1,22;340,290,0,22;100,370,0,28;50,360,0,28;400,230,0,38;140,380,0,38;100,410,0,38;100,400,1,38;290,720,1,31;530,580,1,31;80,410,1,33;470,480,0,33;310,410,1,10;480,210,0,25;400,480,0,25;170,310,0,25;460,480,0,25;410,430,0,19;920,270,0,19;1130,460,0,19;170,450,1,19;110,440,0,16;50,390,1,16;130,370,0,20;330,300,0,20;540,350,0,12;560,330,0,12;100,330,0,12;90,380,0,21;210,320,0,21;200,420,0,21;220,320,1,21;80,400,0,21;100,330,0,17;1100,350,0,17;520,510,0,15;40,350,0,15;460,490,0,15\n"
"Bernard Sarppong Somuah|970,660,0,30;590,600,0,30;1120,440,0,30;860,180,0,30;610,180,0,24;680,130,0,24;890,230,0,24;680,160,0,23;830,160,0,23;590,180,0,9;820,310,0,9;560,540,0,34;700,460,0,34;500,720,0,34;800,530,0,1;660,540,0,1;340,40,0,13;970,340,0,13;760,470,0,13;740,780,0,13;490,210,0,3;650,670,0,3;1030,500,0,3;1120,400,0,32;700,410,0,32;660,640,0,32;740,470,0,36;920,210,0,35;1140,420,0,35;660,190,0,22;580,70,0,22;940,520,0,22;830,380,0,28;610,120,0,38;740,290,0,38;650,540,0,37;1160,380,0,37;880,290,0,19;760,410,0,27;730,570,0,20;1060,430,0,20;470,380,0,8;1140,410,0,8;710,490,0,8;1120,470,0,8;550,390,0,8;1100,460,0,29;1150,410,0,29;730,560,0,12;840,240,0,12;740,270,0,21;530,200,0,21;800,120,0,21;1080,470,0,21;880,290,0,21;690,400,0,21;1000,370,0,17;810,740,0,17\n"
"Anxo Rodriguez Alvarez|320,200,0,24;410,650,0,24;50,500,1,24;470,500,0,24;460,570,1,24;400,700,0,24;80,400,0,9;70,450,0,9;150,160,0,34;320,390,0,34;80,360,1,34;210,290,0,1;290,260,0,1;500,450,0,1;40,440,1,6;70,510,1,3;280,160,0,18;120,340,1,18;1090,460,0,18;250,240,0,36;260,210,1,36;460,150,0,36;500,30,0,35;560,260,0,22;90,390,1,22;90,390,1,4;590,130,1,28;490,560,0,28;450,650,0,5;470,340,0,38;490,290,0,33;80,370,1,33;350,210,0,33;480,580,0,37;80,540,1,37;90,450,1,19;500,300,0,19;490,310,0,19;560,240,0,19;550,270,0,19;90,420,1,11;90,420,0,16;720,110,0,27;390,280,0,27;80,360,0,20;290,630,1,20;530,680,0,20;390,660,1,20;350,440,0,29;540,550,0,29;110,350,0,21;100,290,1,21;550,110,0,21;350,680,0,21;270,740,0,21;500,590,0,17;590,390,0,15\n"
"Pablo Gavian Alonso|540,650,0,23;1110,450,0,7;100,430,0,7;180,700,1,7;100,390,0,9;470,650,0,9;350,580,0,34;100,430,0,1;530,760,0,6;90,310,0,3;490,730,0,32;540,740,0,18;410,580,1,18;340,620,0,18;270,660,0,18;550,230,0,36;430,750,0,36;460,770,1,35;570,740,0,35;100,460,1,22;910,720,0,28;570,770,0,28;600,600,0,28;380,780,1,5;480,730,1,5;490,740,1,5;1050,380,0,5;50,540,0,33;270,690,0,37;400,750,0,37;680,630,0,11;500,650,1,11;440,660,0,11;780,690,0,11;860,710,0,11;460,760,0,11;1040,590,0,11;160,500,0,20;250,390,1,20;60,390,1,20;70,420,1,8;180,640,1,8;90,590,1,29;750,600,0,12;690,710,0,12\n"
"Álvaro Marín Sesma|750,580,0,24;730,510,0,24;1140,370,0,34;550,500,0,1;1130,320,0,13;750,510,0,13;460,500,0,13;770,640,0,3;400,530,0,18;750,620,0,18;1160,340,0,18;300,220,1,18;960,530,0,36;540,480,0,36;630,620,0,22;70,390,1,22;780,510,0,5;730,510,0,5;680,430,0,33;420,760,0,10;1160,460,0,10;810,290,0,25;1110,400,0,25;930,330,0,25;720,200,0,25;590,100,0,19;630,260,0,19;1020,420,0,19;820,560,0,11;450,730,0,11;770,580,0,11;590,360,0,11;790,560,0,11;820,580,0,20;950,140,0,29;850,250,0,29;840,300,0,29;500,110,0,12;870,400,0,12;870,210,0,21;160,410,0,15\n"
"Óscar Marcos Santamaría|780,320,0,7;1110,330,0,7;720,310,0,9;760,440,0,9;940,120,0,9;450,520,0,34;700,210,0,13;80,420,1,6;770,190,0,6;650,490,0,3;630,600,0,32;1110,350,0,18;650,130,0,36;750,60,0,28;760,360,0,28;1040,130,0,5;710,350,0,5;550,760,0,33;430,580,0,33;300,110,0,10;500,120,0,25;1060,330,0,19;380,530,0,11;680,220,0,12;660,360,0,21;710,190,0,21;480,600,0,15\n"
"Jaime Vázquez Cuervo-Arango|420,80,1,9;240,320,0,13;100,300,0,13;80,310,0,13;130,520,0,13;1170,300,0,13;480,140,0,13;320,50,1,32;440,400,0,25;270,270,1,25;490,410,0,25;140,250,0,11;480,420,0,11;160,340,0,11;60,360,1,16;80,350,1,16;560,410,0,27;420,90,1,20;90,410,0,12;90,380,1,12;860,110,0,21;70,390,0,17;710,320,0,17;90,370,1,17;560,260,1,15\n"
"Adrià Capdevila Puigmal|470,300,0,24;140,480,0,7;30,240,0,7;400,490,0,34;570,490,0,34;980,460,0,13;620,410,0,13;780,510,0,13;400,550,0,13;800,560,0,36;650,390,0,36;500,520,0,36;800,210,0,38;120,400,0,38;140,440,0,38;610,580,0,33;470,590,0,10;180,280,0,19;660,290,0,16;360,630,0,20;310,650,0,20;150,420,1,29;410,740,0,21\n"
"David De la Iglesia Rey|740,240,0,23;680,290,0,23;480,580,0,23;520,630,1,23;570,410,0,23;620,330,0,34;750,530,0,13;490,210,1,18;390,450,0,18;350,180,0,22;400,320,0,22;530,270,0,22;690,150,0,38;590,190,0,38;110,390,0,33;450,530,0,33;520,470,0,25;540,200,0,25;550,520,0,25;490,200,0,25;460,200,0,25;390,580,0,11;460,460,0,20\n"
"Hugo González Sotos|830,660,0,24;800,510,0,23;570,510,0,7;530,600,0,9;900,610,0,13;710,530,0,13;940,550,0,6;850,180,0,6;520,670,0,3;1090,430,0,36;590,610,0,36;650,600,0,28;670,500,0,28;840,390,0,28;800,660,0,28;500,780,0,5;990,200,0,37;700,570,0,29;600,510,0,12;70,470,0,12;730,470,0,15;980,610,0,15\n"
"Hugo Burcio García|1080,370,0,30;510,540,0,24;60,410,1,34;780,530,0,6;1150,320,0,32;500,600,0,18;780,240,0,18;120,550,1,36;370,220,0,36;570,270,0,36;470,180,0,22;510,600,0,31;420,590,0,33;520,740,0,10;350,410,1,10;470,210,0,10;870,190,0,19;550,380,0,19;120,450,1,19;490,290,0,11\n"
"Enrique Ribes Recaj|220,440,0,30;430,530,0,23;400,580,0,23;350,630,0,23;180,660,1,23;400,600,0,23;40,350,1,32;80,400,1,32;250,520,0,36;560,740,0,36;590,530,0,36;1170,400,0,35;1150,430,0,28;190,270,0,38;420,710,0,38;570,690,0,31;60,340,0,25;40,510,1,25\n"
"Ángel Arcos Cadilla|290,160,0,24;360,80,0,13;420,100,1,18;950,170,0,36;490,100,0,36;770,120,0,36;720,50,0,22;130,260,0,4;550,310,0,38;710,70,0,33;1000,260,0,25;460,100,0,19;330,20,0,19;1150,350,0,16;630,200,0,20;340,290,0,12;520,170,0,17\n"
"Andrés Antañón Vieites|740,200,0,7;370,240,0,9;640,450,0,13;780,650,0,13;480,580,0,18;1190,490,0,22;690,240,0,38;150,470,0,38;780,450,0,33;740,370,0,33;350,360,0,10;370,560,0,37;440,290,0,11;1120,360,0,11;590,690,0,20;400,390,0,12\n"
"Frank Germain Jonathan Miller|430,710,0,7;1150,460,0,13;90,450,0,3;130,450,0,3;370,740,1,18;450,740,1,18;80,480,1,18;400,550,1,18;130,480,0,18;660,770,0,10;210,750,1,10;430,750,0,10;680,630,0,19;440,670,1,21;290,770,1,21\n"
"Jan Oliveras Codina|930,720,0,30;100,310,0,30;790,320,0,23;170,200,1,23;240,230,1,23;500,70,0,34;270,320,0,34;570,170,0,13;830,220,0,32;480,110,0,32;650,70,0,28;370,130,1,33;60,360,1,25;220,450,1,37;130,120,1,21\n"
"Joel López Salguero|100,380,0,3;110,440,1,3;240,210,1,18;50,410,1,36;40,270,0,5;700,30,0,38;690,100,0,38;90,390,0,19;200,110,0,11;60,400,0,16;70,320,0,20;530,200,0,20;180,60,1,20\n"
"Jorge Perez-Lafuente Rey|750,530,0,34;810,370,0,34;980,540,0,34;1130,360,0,18;1000,530,0,22;800,620,0,28;1010,570,0,28;820,680,0,28;1130,350,0,19;1120,440,0,29\n"
"Anthony Michel Khayat|740,640,0,13;670,70,0,13;710,780,0,32;580,550,0,31;400,670,0,16;260,460,0,29;120,270,1,29;70,450,0,17\n"
"Aldrine Kipchirchir Kibet|1010,540,0,34;790,60,0,38;730,40,0,38;680,60,0,38;950,350,0,27;730,460,0,27\n"
"Cristian Roberto Carro Arceo|200,460,0,7;440,610,0,8;1020,610,0,15\n"
"Iago Barreiros Núñez|560,610,0,20;1090,360,0,20;890,630,0,21\n"
"Ianis Târbă|890,490,0,7"
)


# ─────────────────────────────────────────────────────────────────────────────
# Position lookup (from previous extraction)
# ─────────────────────────────────────────────────────────────────────────────
POS923 = {
    "Borja Valle Balonga":"Left Midfield","Germán Novoa Enríquez":"Left Center Back",
    "Josep Miguel Fernández Codina":"Right Wing","Eneko Undabarrena Ubillos":"Right Center Back",
    "José Luis Cortés Sen":"Left Center Forward","Pau Ferrer Besalduch":"Center Attacking Midfield",
    "Borja Vázquez  Doña":"Right Center Forward","Andoni López Saratxo":"Left Back",
    "Abdoulaye Keita Keita":"Left Center Forward","David Andújar Jiménez":"Right Center Back",
    "Boris Sébastien Moltenis":"Right Midfield","Eugene Adjei Frimpong":"Left Defensive Midfield",
    "Borislav Ivaylov Stankov":"Center Attacking Midfield","Carlos Calderón López":"Right Midfield",
    "Jorge Iglesias González":"Right Back","Eneko Aguilar Elizalde":"Left Defensive Midfield",
    "Mario Jorrín González":"Right Back","Federico San Emeterio Díaz":"Left Center Midfield",
    "Vicente Esquerdo Santas":"Right Defensive Midfield","Diego Moreno Garbayo":"Right Back",
    "Stivan Petkov":"Center Forward","Vasco Pereira de Sousa":"Left Back",
    "Vladyslav Kysil":"Right Defensive Midfield","Sergio Benito Crujera":"Center Forward",
    "Alejandro Miguel Mula Sanchez":"Left Wing","Erik Morán Arribas":"Right Defensive Midfield",
}

POS8733 = {
    "Pablo González Meixús":"Center Back","Bernard Sarppong Somuah":"Center Forward",
    "Anxo Rodriguez Alvarez":"Left Center Back","Pablo Gavian Alonso":"Right Wing Back",
    "Álvaro Marín Sesma":"Center Forward","Óscar Marcos Santamaría":"Left Center Midfield",
    "Jaime Vázquez Cuervo-Arango":"Left Center Back","Adrià Capdevila Puigmal":"Right Defensive Midfield",
    "David De la Iglesia Rey":"Left Center Midfield","Hugo González Sotos":"Right Wing",
    "Hugo Burcio García":"Left Defensive Midfield","Enrique Ribes Recaj":"Left Center Back",
    "Ángel Arcos Cadilla":"Left Wing Back","Andrés Antañón Vieites":"Left Defensive Midfield",
    "Jan Oliveras Codina":"Right Back","Frank Germain Jonathan Miller":"Right Back",
    "Joel López Salguero":"Left Back","Jorge Perez-Lafuente Rey":"Center Forward",
    "Anthony Michel Khayat":"Right Center Back","Aldrine Kipchirchir Kibet":"Right Wing",
    "Cristian Roberto Carro Arceo":"Right Midfield","Iago Barreiros Núñez":"Right Defensive Midfield",
    "Ianis Târbă":"Center Forward","Seyni Mbaye Ndiaye":"Center Back","Luis Bilbao Aréchaga":"Right Wing",
}


def process_team(pd_raw, pos_map):
    players, jset = [], set()
    for line in pd_raw.strip().split('\n'):
        pipe = line.find('|')
        if pipe < 0: continue
        name = line[:pipe]
        locs_str = line[pipe+1:]
        if not locs_str: continue
        att = won = lost = att_z = mid = def_ = 0
        for loc in locs_str.split(';'):
            if not loc: continue
            p = loc.split(',')
            if len(p) != 4: continue
            try:
                x = int(p[0]) / 10
                w = int(p[2])
                j = int(p[3])
            except: continue
            att += 1
            if w: won += 1
            else: lost += 1
            if x >= 80: att_z += 1
            elif x >= 40: mid += 1
            else: def_ += 1
            jset.add(j)
        if att == 0: continue
        players.append({"name": name, "pos": pos_map.get(name, ""),
                        "att": att, "won": won, "lost": lost,
                        "att_z": att_z, "mid": mid, "def": def_,
                        "locs": locs_str})
    players.sort(key=lambda p: p['att'], reverse=True)
    return {"players": players, "jornadas": sorted(jset)}


da923  = process_team(PD923, POS923)
da8733 = process_team(PD8733, POS8733)

print(f"DA_923:  {len(da923['players'])} players, jornadas {da923['jornadas'][:3]}…{da923['jornadas'][-3:]}")
print(f"DA_8733: {len(da8733['players'])} players, jornadas {da8733['jornadas'][:3]}…{da8733['jornadas'][-3:]}")

js_923  = "  const DA_923 = "  + json.dumps(da923,  ensure_ascii=False, separators=(',',':')) + ";"
js_8733 = "  const DA_8733 = " + json.dumps(da8733, ensure_ascii=False, separators=(',',':')) + ";"

# ─────────────────────────────────────────────────────────────────────────────
# New renderDuelosAereos  (per-player locs + click-to-highlight)
# ─────────────────────────────────────────────────────────────────────────────
NEW_RENDER = r"""  let _daSubTab = 'campo';
  let _daJornada = 'all';
  let _daPlayer  = null;

  function loadDuelosAereos() {
    _daSubTab = 'campo';
    _daJornada = 'all';
    _daPlayer  = null;
    renderDuelosAereos();
  }

  function renderDuelosAereos() {
    const cont = document.getElementById('content');
    if (!cont) return;
    const tid = currentTeam.id;
    const DA_MAP = {923: typeof DA_923!=='undefined'?DA_923:null, 8733: typeof DA_8733!=='undefined'?DA_8733:null};
    const data = DA_MAP[tid];
    const resCol = r => r==='W'?'#3fb950':r==='D'?'#e3b341':r==='L'?'#f85149':'var(--text3)';

    const tabBtn = (id, label) => {
      const act = _daSubTab === id;
      return `<button onclick="_daSubTab='${id}';renderDuelosAereos()" style="background:none;border:none;border-bottom:2px solid ${act?'var(--accent)':'transparent'};color:${act?'var(--text1)':'var(--text3)'};font-size:13px;font-weight:${act?700:400};padding:11px 16px;cursor:pointer;font-family:inherit;letter-spacing:.3px;transition:all .15s">${label}</button>`;
    };
    const tabBar = `<div style="border-bottom:1px solid var(--border);padding:0 24px;background:var(--bg1);display:flex;gap:0;flex-shrink:0">
      ${tabBtn('campo','Campo')}
      ${tabBtn('jugadores','Jugadores')}
    </div>`;

    if (!data) {
      cont.innerHTML = `<div style="height:100%;display:flex;flex-direction:column;overflow:hidden">${tabBar}<div style="flex:1;display:flex;align-items:center;justify-content:center;color:var(--text3);font-size:13px">Datos próximamente</div></div>`;
      return;
    }

    // Helper: parse compact locs string → [{x,y,won,j}]
    function parseLocs(s) {
      return (s||'').split(';').filter(Boolean).map(e=>{
        const p=e.split(',');
        return {x:parseInt(p[0])/10,y:parseInt(p[1])/10,won:+p[2],j:+p[3]};
      });
    }

    // Build match metadata
    const matchMeta = {};
    if (tid === 923) {
      const pts = (typeof PARTIDOS_MAP !== 'undefined' && PARTIDOS_MAP[923]) || [];
      pts.forEach(p => {
        const jn = parseInt((p.j||'').replace(/\D/g,''), 10);
        if (!jn) return;
        const isHome = !!(p.local && p.local.includes('Ponferradina'));
        const rival = isHome ? (p.vis||'') : (p.local||'');
        const sc = p.s || '?-?';
        const [gl,gv] = sc.split('-').map(Number);
        const myG = isHome ? gl : gv, thG = isHome ? gv : gl;
        const res = isNaN(myG)||isNaN(thG) ? '?' : myG>thG?'W':myG<thG?'L':'D';
        matchMeta[jn] = {isHome, rival, score:sc, res};
      });
    } else {
      const xd = typeof XLOSS_8733 !== 'undefined' ? XLOSS_8733 : [];
      xd.forEach(p => {
        const jn = parseInt((p.j||'').replace(/\D/g,''), 10);
        if (!jn) return;
        const isHome = p.loc === 'L';
        matchMeta[jn] = {isHome, rival: p.rival||'', score: p.score||'?-?', res: p.res||'?'};
      });
    }

    // Compute locs: either selected player or all players
    const selPlayer = _daPlayer ? data.players.find(p=>p.name===_daPlayer) : null;
    const baseLocs = selPlayer
      ? parseLocs(selPlayer.locs)
      : data.players.flatMap(p=>parseLocs(p.locs));
    const allLocs = _daJornada==='all' ? baseLocs : baseLocs.filter(l=>l.j===_daJornada);
    const totAtt = allLocs.length;
    const totWon = allLocs.filter(l=>l.won).length;
    const totPct = totAtt ? Math.round(totWon/totAtt*100) : 0;

    // Match panel
    const jornadas = data.jornadas || [];
    const curLabel = _daJornada==='all' ? 'TODAS' : 'J'+_daJornada;
    const todasSel = _daJornada === 'all';
    const allLocsFlat = data.players.flatMap(p=>parseLocs(p.locs));
    const todasChip = `<button onclick="_daJornada='all';renderDuelosAereos()"
      style="background:${todasSel?'rgba(88,166,255,0.1)':'var(--bg3)'};border:1px solid ${todasSel?'rgba(88,166,255,0.5)':'var(--border)'};color:${todasSel?'var(--blue)':'var(--text2)'};padding:6px 10px;border-radius:6px;font-family:inherit;font-size:11px;cursor:pointer;transition:all 0.15s;text-align:left;display:flex;flex-direction:column;gap:2px;min-width:88px">
      <span style="font-weight:800;font-size:11px;color:${todasSel?'var(--blue)':'var(--accent)'}">TODAS</span>
      <span style="font-size:10px;color:var(--text3)">${allLocsFlat.length} duelos</span>
      <span style="font-size:10px">&nbsp;</span>
    </button>`;
    const matchChips = jornadas.map(j => {
      const sel = _daJornada === j;
      const m = matchMeta[j];
      const rc = m ? resCol(m.res) : 'var(--text3)';
      const icon = m ? (m.isHome ? '🏠' : '✈️') : '';
      const rivalTxt = m ? (m.rival.length>14 ? m.rival.substring(0,12)+'…' : m.rival) : '—';
      const scoreTxt = m ? m.score : '';
      return `<button onclick="_daJornada=${j};renderDuelosAereos()"
        style="background:${sel?'rgba(88,166,255,0.1)':'var(--bg3)'};border:1px solid ${sel?'rgba(88,166,255,0.5)':'var(--border)'};color:${sel?'var(--blue)':'var(--text2)'};padding:6px 10px;border-radius:6px;font-family:inherit;font-size:11px;cursor:pointer;transition:all 0.15s;text-align:left;display:flex;flex-direction:column;gap:2px;min-width:88px">
        <span style="font-weight:700;font-size:10px;color:${sel?'var(--blue)':'var(--accent)'}">J${j}</span>
        <span style="font-size:10px">${icon} ${rivalTxt}</span>
        <span style="font-size:10px;font-weight:700;color:${rc}">${scoreTxt}</span>
      </button>`;
    }).join('');
    const matchPanel = `<div style="background:var(--bg2);border:1px solid rgba(88,166,255,0.2);border-radius:10px;padding:12px 14px;margin-bottom:14px">
      <div style="font-size:10px;color:var(--blue);letter-spacing:1.5px;text-transform:uppercase;font-weight:600;margin-bottom:10px">
        SELECCIONA UN PARTIDO · <span style="color:var(--text2)">${currentTeam.name} (${curLabel})</span>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px">${todasChip}${matchChips}</div>
    </div>`;

    // Match bar (when a jornada is selected)
    let matchBar = '';
    if (_daJornada !== 'all') {
      const m = matchMeta[_daJornada];
      if (m) {
        const rc = resCol(m.res);
        const resLabel = m.res==='W'?'VICTORIA':m.res==='D'?'EMPATE':'DERROTA';
        matchBar = `<div style="display:flex;align-items:center;gap:12px;padding:7px 12px;background:var(--bg2);border:1px solid var(--border);border-radius:8px;margin-bottom:10px;flex-wrap:wrap">
          <span style="font-size:11px;font-weight:700;color:var(--accent)">J${_daJornada}</span>
          <span style="font-size:13px;color:var(--text1);font-weight:500">${m.isHome?'🏠':'✈️'} ${m.rival}</span>
          <span style="font-family:'Bebas Neue',sans-serif;font-size:18px;color:${rc}">${m.score}</span>
          <span style="font-size:9px;font-weight:700;color:${rc};background:${rc}22;padding:2px 7px;border-radius:4px">${resLabel}</span>
          <span style="font-size:10px;color:var(--text3);margin-left:auto">${totAtt} duelos · <span style="color:#3fb950">${totWon} gan</span> · <span style="color:#f85149">${totAtt-totWon} perd</span> · <span style="color:${totPct>=50?'#3fb950':totPct>=30?'#e3b341':'#f85149'}">${totPct}%</span></span>
        </div>`;
      }
    }

    // ── Jugadores tab ────────────────────────────────────────────────────────
    if (_daSubTab === 'jugadores') {
      const players = [...data.players].sort((a,b)=>b.att-a.att);
      const maxAtt = players[0]?.att||1;
      const rows = players.map((p,i)=>{
        const pct=p.att?Math.round(p.won/p.att*100):0;
        const col=pct>=50?'#3fb950':pct>=30?'#e3b341':'#f85149';
        const totZ=(p.att_z||0)+(p.mid||0)+(p.def||0)||1;
        const zBar=(val,c)=>val?`<div style="height:4px;background:${c};border-radius:2px;width:${Math.round(val/totZ*60)}px;flex-shrink:0"></div>`:'';
        return `<tr style="border-bottom:1px solid var(--border)" onmouseenter="this.style.background='var(--bg3)'" onmouseleave="this.style.background=''">
          <td style="padding:8px;font-size:11px;color:var(--text3);width:20px">${i+1}</td>
          <td style="padding:8px"><div style="font-size:12px;font-weight:700;color:var(--text1)">${p.name}</div><div style="font-size:10px;color:var(--text3)">${p.pos}</div></td>
          <td style="padding:8px;min-width:100px"><div style="display:flex;align-items:center;gap:6px"><div style="flex:1;height:5px;background:var(--bg3);border-radius:3px"><div style="height:5px;background:var(--accent);border-radius:3px;width:${Math.round(p.att/maxAtt*100)}%"></div></div><span style="font-size:12px;font-weight:700;color:var(--text1);min-width:18px;text-align:right">${p.att}</span></div></td>
          <td style="padding:8px;font-size:12px;color:#3fb950;text-align:center;font-weight:600">${p.won}</td>
          <td style="padding:8px;font-size:12px;color:#f85149;text-align:center;font-weight:600">${p.lost}</td>
          <td style="padding:8px;font-size:13px;font-weight:700;text-align:center;color:${col}">${pct}%</td>
          <td style="padding:8px"><div style="font-size:9px;color:var(--text3);margin-bottom:3px">${p.att_z||0} ATQ · ${p.mid||0} MED · ${p.def||0} DEF</div><div style="display:flex;gap:2px;align-items:center">${zBar(p.att_z,'#3fb950')}${zBar(p.mid,'#e3b341')}${zBar(p.def,'#58a6ff')}</div></td>
        </tr>`;
      }).join('');
      cont.innerHTML=`<div style="height:100%;display:flex;flex-direction:column;overflow:hidden">${tabBar}<div style="flex:1;overflow-y:auto;padding:14px 18px">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
          <img src="${currentTeam.escudo}" style="width:22px;height:22px;object-fit:contain"/>
          <span style="font-size:12px;font-weight:800;color:var(--text1)">DUELOS AÉREOS — ${currentTeam.name.toUpperCase()}</span>
          <span style="font-size:10px;color:var(--text3)">Temporada 2025/26</span>
        </div>
        ${matchPanel}
        ${matchBar}
        <table style="width:100%;border-collapse:collapse"><thead><tr style="border-bottom:2px solid var(--border)"><th style="padding:7px 8px;font-size:10px;color:var(--text3);font-weight:600;text-align:left">#</th><th style="padding:7px 8px;font-size:10px;color:var(--text3);font-weight:600;text-align:left">JUGADOR</th><th style="padding:7px 8px;font-size:10px;color:var(--text3);font-weight:600;text-align:left">DUELOS</th><th style="padding:7px 8px;font-size:10px;color:#3fb950;font-weight:600;text-align:center">GAN.</th><th style="padding:7px 8px;font-size:10px;color:#f85149;font-weight:600;text-align:center">PERD.</th><th style="padding:7px 8px;font-size:10px;color:var(--text3);font-weight:600;text-align:center">%</th><th style="padding:7px 8px;font-size:10px;color:var(--text3);font-weight:600;text-align:left">POR ZONA</th></tr></thead><tbody>${rows}</tbody></table>
      </div></div>`;
      return;
    }

    // ── Campo: dos medio campos ──────────────────────────────────────────────
    const defLocs = allLocs.filter(l=>l.x<60);
    const offLocs = allLocs.filter(l=>l.x>=60);

    const W=270, H=324;
    const DZONES=[{x0:0,x1:20,lbl:'DEF'},{x0:20,x1:40,lbl:'MED'},{x0:40,x1:60,lbl:'ENT'}];
    const OZONES=[{x0:60,x1:80,lbl:'SAL'},{x0:80,x1:100,lbl:'ATQ'},{x0:100,x1:120,lbl:'GOL'}];
    const LANES=[{y0:0,y1:16,lbl:'BI'},{y0:16,y1:32,lbl:'II'},{y0:32,y1:48,lbl:'CEN'},{y0:48,y1:64,lbl:'ID'},{y0:64,y1:80,lbl:'BD'}];

    function buildHalfPitch(locs, zones, xOffset, isOff) {
      const sx=W/60, zW=W/3, lH=H/5, sy=H/80;
      const cells=zones.flatMap((z)=>LANES.map((l)=>{
        const cl=locs.filter(loc=>loc.x>=z.x0&&loc.x<z.x1&&loc.y>=l.y0&&loc.y<l.y1);
        const total=cl.length,won=cl.filter(loc=>loc.won).length;
        const pct=total?Math.round(won/total*100):null;
        return {total,won,pct,px0:(z.x0-xOffset)*sx,py0:l.y0*sy};
      }));
      const cellBgs=cells.map(c=>{
        if(!c.total) return '';
        const col=c.pct>=50?'#3fb950':c.pct>=30?'#e3b341':'#f85149';
        return `<rect x="${c.px0.toFixed(1)}" y="${c.py0.toFixed(1)}" width="${zW.toFixed(1)}" height="${lH.toFixed(1)}" fill="${col}" opacity="0.13"/>`;
      }).join('');
      const dotR = selPlayer ? '4' : '3';
      const dots=locs.filter(l=>!l.won).map(l=>`<circle cx="${((l.x-xOffset)*sx).toFixed(1)}" cy="${(l.y*sy).toFixed(1)}" r="${dotR}" fill="#f85149" fill-opacity="0.85"/>`).join('')
               +locs.filter(l=>l.won).map(l=>`<circle cx="${((l.x-xOffset)*sx).toFixed(1)}" cy="${(l.y*sy).toFixed(1)}" r="${dotR}" fill="#3fb950" fill-opacity="0.85"/>`).join('');
      const cellTexts=cells.map(c=>{
        if(!c.total) return '';
        const cx=(c.px0+zW/2).toFixed(1),cy0=c.py0+lH/2;
        const col=c.pct>=50?'#7ee787':c.pct>=30?'#f0c040':'#ff8080';
        return `<rect x="${(c.px0+zW/2-20).toFixed(1)}" y="${(cy0-12).toFixed(1)}" width="40" height="20" rx="3" fill="rgba(0,0,0,0.55)"/>
<text x="${cx}" y="${(cy0-1).toFixed(1)}" text-anchor="middle" fill="rgba(255,255,255,0.85)" font-size="7.5" font-family="DM Sans">${c.won}/${c.total}</text>
<text x="${cx}" y="${(cy0+9).toFixed(1)}" text-anchor="middle" fill="${col}" font-size="9.5" font-weight="700" font-family="DM Sans">${c.pct}%</text>`;
      }).join('');
      const zLines=[20,40].map(x=>`<line x1="${((x-xOffset)*sx).toFixed(1)}" y1="0" x2="${((x-xOffset)*sx).toFixed(1)}" y2="${H}" stroke="rgba(255,255,255,0.5)" stroke-width="1.2" stroke-dasharray="5,3"/>`).join('');
      const lLines=[16,32,48,64].map(y=>`<line x1="0" y1="${(y*sy).toFixed(1)}" x2="${W}" y2="${(y*sy).toFixed(1)}" stroke="rgba(255,255,255,0.3)" stroke-width="0.8" stroke-dasharray="3,3"/>`).join('');
      const zLabels=zones.map((z)=>`<text x="${((z.x0-xOffset+(z.x1-z.x0)/2)*sx).toFixed(1)}" y="12" text-anchor="middle" fill="rgba(255,255,255,0.75)" font-size="9" font-weight="700" font-family="DM Sans">${z.lbl}</text>`).join('');
      const lLabels=LANES.map(l=>`<text x="4" y="${((l.y0+l.y1)/2*sy+3).toFixed(1)}" fill="rgba(255,255,255,0.45)" font-size="7" font-family="DM Sans">${l.lbl}</text>`).join('');
      let pArea='';
      if(!isOff){
        pArea=`<rect x="0" y="${((80-40.32)/2*sy).toFixed(1)}" width="${(16.5*sx).toFixed(1)}" height="${(40.32*sy).toFixed(1)}" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="0.9"/>
<rect x="0" y="${((80-18.32)/2*sy).toFixed(1)}" width="${(5.5*sx).toFixed(1)}" height="${(18.32*sy).toFixed(1)}" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="0.7"/>`;
      } else {
        pArea=`<rect x="${((103.5-xOffset)*sx).toFixed(1)}" y="${((80-40.32)/2*sy).toFixed(1)}" width="${(16.5*sx).toFixed(1)}" height="${(40.32*sy).toFixed(1)}" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="0.9"/>
<rect x="${((114.5-xOffset)*sx).toFixed(1)}" y="${((80-18.32)/2*sy).toFixed(1)}" width="${(5.5*sx).toFixed(1)}" height="${(18.32*sy).toFixed(1)}" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="0.7"/>`;
      }
      return `<svg width="${W}" height="${H}" style="display:block;border-radius:${isOff?'0 8px 8px 0':'8px 0 0 8px'};overflow:hidden;flex-shrink:0">
  ${[0,1,2,3,4,5,6].map(i=>`<rect x="0" y="${(i*H/7).toFixed(1)}" width="${W}" height="${(H/7).toFixed(1)}" fill="${i%2===0?'#2a5c1a':'#265618'}"/>`).join('')}
  ${cellBgs}<rect x="0" y="0" width="${W}" height="${H}" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.2"/>
  ${pArea}${zLines}${lLines}${zLabels}${lLabels}${dots}${cellTexts}
</svg>`;
    }

    const svgDef=buildHalfPitch(defLocs,DZONES,0,false);
    const svgOff=buildHalfPitch(offLocs,OZONES,60,true);

    const dW=defLocs.filter(l=>l.won).length,dT=defLocs.length,dP=dT?Math.round(dW/dT*100):0;
    const oW=offLocs.filter(l=>l.won).length,oT=offLocs.length,oP=oT?Math.round(oW/oT*100):0;

    const halfLabel = _daJornada==='all' ? 'TODOS LOS PARTIDOS' : 'J'+_daJornada;

    const halfStat=(label,won,total,pct,col)=>`<div style="text-align:center;padding:5px 9px;background:var(--bg2);border:1px solid var(--border);border-radius:6px;min-width:110px">
  <div style="font-size:9px;font-weight:700;color:${col};text-transform:uppercase;letter-spacing:.8px;margin-bottom:3px">${label}</div>
  <div style="display:flex;justify-content:center;gap:8px;align-items:baseline">
    <span style="font-size:14px;font-weight:800;color:#3fb950">${won}<span style="font-size:9px;color:var(--text3)">G</span></span>
    <span style="font-size:14px;font-weight:800;color:#f85149">${total-won}<span style="font-size:9px;color:var(--text3)">P</span></span>
    <span style="font-size:15px;font-weight:800;color:${pct>=50?'#3fb950':pct>=30?'#e3b341':'#f85149'}">${pct}%</span>
  </div>
</div>`;

    // Player banner (when player is selected)
    const playerBanner = selPlayer ? `<div style="display:flex;align-items:center;gap:10px;padding:7px 12px;background:rgba(88,166,255,0.1);border:1px solid rgba(88,166,255,0.35);border-radius:8px;margin-bottom:8px;flex-wrap:wrap">
      <span style="font-size:12px;font-weight:700;color:var(--blue)">👤 ${selPlayer.name}</span>
      <span style="font-size:10px;color:var(--text3)">${totAtt} duelos · ${totWon}G · ${totAtt-totWon}P · ${totPct}%</span>
      <button onclick="_daPlayer=null;renderDuelosAereos()" style="margin-left:auto;background:rgba(248,81,73,0.12);border:1px solid rgba(248,81,73,0.35);color:#f85149;border-radius:4px;padding:2px 8px;font-size:10px;cursor:pointer;font-family:inherit">✕ Ver todos</button>
    </div>` : '';

    // Player sidebar (top 12 by att, clickable)
    const topPlayers = [...data.players].sort((a,b)=>b.won-a.won).slice(0,12);
    const playerRows = topPlayers.map(p=>{
      const pct=p.att?Math.round(p.won/p.att*100):0;
      const col=pct>=50?'#3fb950':pct>=30?'#e3b341':'#f85149';
      const isSel = _daPlayer === p.name;
      const safeName = p.name.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
      return `<div onclick="_daPlayer='${safeName}'===_daPlayer?null:'${safeName}';renderDuelosAereos()"
        style="display:flex;align-items:center;gap:6px;padding:5px 6px;border-bottom:1px solid var(--border);cursor:pointer;background:${isSel?'rgba(88,166,255,0.1)':'transparent'};border-radius:${isSel?'4px':'0'};transition:background 0.15s"
        onmouseenter="if(!${isSel})this.style.background='rgba(88,166,255,0.06)'"
        onmouseleave="this.style.background='${isSel?'rgba(88,166,255,0.1)':'transparent'}'">
        <div style="flex:1;min-width:0">
          <div style="font-size:11px;font-weight:${isSel?800:600};color:${isSel?'var(--blue)':'var(--text1)'};white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="${p.name}">${p.name}</div>
          <div style="font-size:9px;color:var(--text3)">${p.att} duelos</div>
        </div>
        <div style="text-align:right;flex-shrink:0">
          <div style="font-size:12px;font-weight:800;color:${col}">${pct}%</div>
          <div style="font-size:9px;color:var(--text3)">${p.won}G·${p.lost}P</div>
        </div>
      </div>`;
    }).join('');
    const playerSidebar=`<div style="width:180px;flex-shrink:0;margin-left:14px">
      <div style="font-size:9px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;padding-bottom:4px;border-bottom:1px solid var(--border)">TOP JUGADORES · TEMPORADA</div>
      ${playerRows}
    </div>`;

    cont.innerHTML=`<div style="height:100%;display:flex;flex-direction:column;overflow:hidden">
  ${tabBar}
  <div style="flex:1;overflow-y:auto;padding:12px 16px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
      <img src="${currentTeam.escudo}" style="width:22px;height:22px;object-fit:contain;flex-shrink:0"/>
      <span style="font-size:12px;font-weight:800;color:var(--text1)">DUELOS AÉREOS — ${currentTeam.name.toUpperCase()}</span>
      <span style="font-size:10px;color:var(--text3)">Temporada 2025/26 · Primera RFEF</span>
    </div>
    ${matchPanel}
    ${matchBar}
    ${playerBanner}
    <div style="display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap;align-items:center">
      ${halfStat('Defensivos',dW,dT,dP,'#58a6ff')}
      ${halfStat('Ofensivos',oW,oT,oP,'#3fb950')}
      <div style="display:flex;align-items:center;gap:10px;margin-left:auto;flex-wrap:wrap">
        <div style="display:flex;align-items:center;gap:4px;font-size:10px;color:var(--text3)"><span style="width:8px;height:8px;border-radius:50%;background:#3fb950;display:inline-block"></span>Ganado</div>
        <div style="display:flex;align-items:center;gap:4px;font-size:10px;color:var(--text3)"><span style="width:8px;height:8px;border-radius:50%;background:#f85149;display:inline-block"></span>Perdido</div>
      </div>
    </div>
    <div style="display:flex;gap:0;align-items:flex-start">
      <div>
        <div style="font-size:10px;font-weight:700;color:#58a6ff;text-align:center;margin-bottom:4px;letter-spacing:.5px">DUELOS DEFENSIVOS · ${halfLabel}</div>
        ${svgDef}
      </div>
      <div>
        <div style="font-size:10px;font-weight:700;color:#3fb950;text-align:center;margin-bottom:4px;letter-spacing:.5px">DUELOS OFENSIVOS · ${halfLabel}</div>
        ${svgOff}
      </div>
      ${playerSidebar}
    </div>
  </div>
</div>`;
  }"""

# ─────────────────────────────────────────────────────────────────────────────
# Patch index.html
# ─────────────────────────────────────────────────────────────────────────────
html_path = "/Users/alejandroballesterostamayo/Desktop/tactical/tactical/index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace DA_923
m = re.search(r'  const DA_923 = \{.*?\};', content, re.DOTALL)
if m:
    content = content[:m.start()] + js_923 + content[m.end():]
    print("✅ DA_923 replaced")
else:
    print("❌ DA_923 not found")

# 2. Replace DA_8733
m = re.search(r'  const DA_8733 = \{.*?\};', content, re.DOTALL)
if m:
    content = content[:m.start()] + js_8733 + content[m.end():]
    print("✅ DA_8733 replaced")
else:
    print("❌ DA_8733 not found")

# 3. Replace renderDuelosAereos block
idx_start = content.find("  let _daSubTab = 'campo';")
idx_end   = content.find('\n  // Global: used by both renderLineaDef', idx_start)
if idx_start >= 0 and idx_end > idx_start:
    content = content[:idx_start] + NEW_RENDER + "\n" + content[idx_end:]
    print("✅ renderDuelosAereos replaced")
else:
    print(f"❌ renderDuelosAereos block not found (start={idx_start}, end={idx_end})")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ index.html patched successfully")
