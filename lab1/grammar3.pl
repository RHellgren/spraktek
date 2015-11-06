% Grammatikregler
s --> np.

np --> det(Genus,Species,Numerus,Kasus), jj(Genus,Species,Numerus,Kasus), n(Genus,Species,Numerus,Kasus).
np --> det(Genus,Species,Numerus,Kasus), jj(Genus,Species,Numerus,Kasus), n(Genus,Species,Numerus,Kasus), n(Genus,Species,Numerus,Kasus).

% Lexikon
det(utrum,_,singularis,_) --> [ en ]. 
det(neutrum,_,singularis,_) --> [ ett ]. 
det(_,_,_,_) --> [ den ].
det(_,_,_,_) --> [ det ].
det(_,_,_,_) --> [ några ].
det(_,_,_,_) --> [ de ].

jj(utrum,_,singularis,_) --> [ gammal ]. 
jj(neutrum,_,singularis,_) --> [ gammalt ]. 
jj(neutrum,_,pluralis,_) --> [ gamla ]. 
jj(utrum,_,pluralis,_) --> [ gamla ].
jj(_,_,_,_) --> [ gamle ].

jj(_,_,_,_) --> [ röd ].
jj(_,_,_,_) --> [ rött ].
jj(_,_,_,_) --> [ röde ].
jj(_,_,_,_) --> [ röda ].

n(neutrum,_,singularis,_) --> [ bord ].

n(_,_,_,_) --> [ man ].
n(_,_,_,_) --> [ mannen ].
n(_,_,_,_) --> [ män ].
n(_,_,_,_) --> [ männen ].
n(_,_,_,_) --> [ mans ].
n(_,_,_,_) --> [ mannens ].
n(_,_,_,_) --> [ mäns ].
n(_,_,_,_) --> [ männens ].

n(_,_,_,_) --> [ kvinna ].
n(_,_,_,_) --> [ kvinnan ].
n(_,_,_,_) --> [ kvinnor ].
n(_,_,_,_) --> [ kvinnorna ].
n(_,_,_,_) --> [ kvinnas ].
n(_,_,_,_) --> [ kvinnans ].
n(_,_,_,_) --> [ kvinnors ].
n(_,_,_,_) --> [ kvinnornas ].

n(_,_,_,_) --> [ bordet ].
n(_,_,_,_) --> [ borden ].
n(_,_,_,_) --> [ bords ].
n(_,_,_,_) --> [ bordets ].
n(_,_,_,_) --> [ bordens ].

n(_,_,_,_) --> [ skal ].
n(_,_,_,_) --> [ skalet ].
n(_,_,_,_) --> [ skalen ].
n(_,_,_,_) --> [ skals ].
n(_,_,_,_) --> [ skalets ].
n(_,_,_,_) --> [ skalens ].

n(_,_,_,_) --> [ äpple].
n(_,_,_,_) --> [ äpplet ].
n(_,_,_,_) --> [ äpplen ].
n(_,_,_,_) --> [ äpplena ].
n(_,_,_,_) --> [ äpples ].
n(_,_,_,_) --> [ äpplets ].
n(_,_,_,_) --> [ äpplens ].
n(_,_,_,_) --> [ äpplenas ].

n(_,_,_,_) --> [ kant ].
n(_,_,_,_) --> [ kanten ].
n(_,_,_,_) --> [ kanter ].
n(_,_,_,_) --> [ kanterna ].
n(_,_,_,_) --> [ kants ].
n(_,_,_,_) --> [ kantens ].
n(_,_,_,_) --> [ kanters ].
n(_,_,_,_) --> [ kanternas ].


