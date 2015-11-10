% Grammatikregler
s --> np.

np --> det(Genus,Species,Numerus,Kasus), jj(Genus,Species,Numerus,Kasus), n(Genus,Species,Numerus,nominativ).
np --> det(Genus,Species,Numerus,Kasus), jj(Genus,Species,Numerus,Kasus), n(Genus,Species,Numerus,genitiv), n(_,_,_,nominativ).

% Lexikon
det(utrum,indefinit,singularis,_) --> [ en ]. 
det(neutrum,indefinit,singularis,_) --> [ ett ]. 
det(utrum,definit,singularis,_) --> [ den ].
det(maskulinum,definit,singularis,_) --> [ den ].
det(neutrum,definit,singularis,_) --> [ det ].
det(_,indefinit,pluralis,_) --> [ några ].
det(_,definit,pluralis,_) --> [ de ].

jj(utrum,indefinit,singularis,_) --> [ gammal ]. 
jj(neutrum,indefinit,singularis,_) --> [ gammalt ]. 
jj(_,definit,singularis,_) --> [ gamla ]. 
jj(_,_,pluralis,_) --> [ gamla ].
jj(maskulinum,_,singularis,_) --> [ gamle ].

jj(_,_,singularis,_) --> [ röd ].
jj(_,_,singularis,_) --> [ rött ].
jj(_,definit,singularis,_) --> [ röda ].
jj(_,_,pluralis,_) --> [ röda ].

n(utrum,indefinit,singularis,nominativ) --> [ man ].
n(utrum,definit,singularis,nominativ) --> [ mannen ].
n(maskulinum,definit,singularis,nominativ) --> [ mannen ].
n(_,indefinit,pluralis,nominativ) --> [ män ].
n(_,definit,pluralis,nominativ) --> [ männen ].
n(utrum,indefinit,singularis,genitiv) --> [ mans ].
n(utrum,definit,singularis,genitiv) --> [ mannens ].
n(maskulinum,definit,singularis,genitiv) --> [ mannens ].
n(_,indefinit,pluralis,genitiv) --> [ mäns ].
n(_,definit,pluralis,genitiv) --> [ männens ].

n(utrum,indefinit,singularis,nominativ) --> [ kvinna ].
n(utrum,definit,singularis,nominativ) --> [ kvinnan ].
n(_,indefinit,pluralis,nominativ) --> [ kvinnor ].
n(_,definit,pluralis,nominativ) --> [ kvinnorna ].
n(utrum,indefinit,singularis,genitiv) --> [ kvinnas ].
n(utrum,definit,singularis,genitiv) --> [ kvinnans ].
n(_,indefinit,pluralis,genitiv) --> [ kvinnors ].
n(_,definit,pluralis,genitiv) --> [ kvinnornas ].

n(neutrum,indefinit,_,nominativ) --> [ bord ].
n(neutrum,definit,singularis,nominativ) --> [ bordet ].
n(_,definit,pluralis,nominativ) --> [ borden ].
n(neutrum,indefinit,_,genitiv) --> [ bords ].
n(neutrum,definit,singularis,genitiv) --> [ bordets ].
n(_,definit,pluralis,genitiv) --> [ bordens ].

n(neutrum,indefinit,_,nominativ) --> [ skal ].
n(neutrum,definit,singularis,nominativ) --> [ skalet ].
n(_,definit,pluralis,nominativ) --> [ skalen ].
n(_,indefinit,_,genitiv) --> [ skals ].
n(neutrum,definit,singularis,genitiv) --> [ skalets ].
n(_,definit,pluralis,genitiv) --> [ skalens ].

n(neutrum,indefinit,singularis,nominativ) --> [ äpple].
n(neutrum,definit,singularis,nominativ) --> [ äpplet ].
n(_,indefinit,pluralis,nominativ) --> [ äpplen ].
n(_,definit,pluralis,nominativ) --> [ äpplena ].
n(neutrum,indefinit,singularis,genitiv) --> [ äpples ].
n(neutrum,definit,singularis,genitiv) --> [ äpplets ].
n(_,indefinit,pluralis,genitiv) --> [ äpplens ].
n(_,definit,pluralis,genitiv) --> [ äpplenas ].

n(utrum,indefinit,singularis,nominativ) --> [ kant ].
n(utrum,definit,singularis,nominativ) --> [ kanten ].
n(_,indefinit,pluralis,nominativ) --> [ kanter ].
n(_,definit,pluralis,nominativ) --> [ kanterna ].
n(utrum,indefinit,singularis,genitiv) --> [ kants ].
n(utrum,definit,singularis,genitiv) --> [ kantens ].
n(_,indefinit,pluralis,genitiv) --> [ kanters ].
n(_,definit,pluralis,genitiv) --> [ kanternas ].


