<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8" />
    <title>Annotateur</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'home_page.css' %}">
</head>
<body>

  <!-- Barre de navigation --> 
  <nav>
    <div class="nav-content">
    <div class="logo">
        <a >CYPS Genome Annotation.</a> 
    </div>
    <ul class="nav-links">
        <li><a href="/">Acceuil</a></li>
        <li><a href="annot_seq.html">Choisir une séquence à annoter</a></li>
        <li><a href="annot_history.html">Historique des Annotations</a></li>
        <li><a href="logout.html">Se deconnecter</a></li>
    </ul>
    </div>
  </nav>

  <section class="home"></section>
  <div class="text">
    <p><h2> Tu es Annotateur tu as plusieurs fonctionnalités ! </h2><br>
        <p>Clique sur <strong>Choisir une séquence à annoter</strong> pour choisir une séquence à annoter. Après avoir choisi une séquence, tu pourras remplir plusieurs catégories afin d'annoter ta séquence. Tu peux vérifier l'historique des annotations.</p><br>
        <button class='btn btn--assign' type='submit' onclick = "location.href = 'annot_seq.html'">Choose a sequence to annotate</button>    
  </div>
<!-- Logo -->
  <script>
let nav = document.querySelector("nav");
    window.onscroll = function() {
        if(document.documentElement.scrollTop > 20){
            nav.classList.add("sticky");
        }else {
            nav.classList.remove("sticky");
        }
    }
  </script>
</body>
</html>


<nav><!--Navigation menu-->
    <div class="nav-content">
        <div class="logo">
            <a href="Home_page.html">GenAnnot.</a>
        </div>
        <ul class="nav-links">
            <li><a href="/">Acceuil</a></li>
            <li><a href="annot_seq.html">Choisir une séquence à annoter</a></li>
            <li><a href="annot_history.html">Historique des Annotations</a></li>
            <li><a href="logout.html">Se deconnecter</a></li>
        </ul>
    </div>
</nav>
<div class ="container">
    <p><h2> This is the Annotator page ! </h2><br>
    <p>Click on <strong>Choose a sequence to annotate</strong> to annotate a sequence. After a sequence is choosen, it leads to the Annotation form. You can check your annotations history.</p><br>
    <button class='btn btn--assign' type='submit' onclick = "location.href = 'annot_seq.html'">Choose a sequence to annotate</button>
</div>
</body>
</html>
