console.clear()
const elempot = []
table=document.getElementsByClassName("wikitable")[0].rows
for ( var i=1; i<table.length; i++){
  boldtext=table[i].firstElementChild.innerHTML.slice(-1)
  if (boldtext == ">"){
    console.log(table[i].firstElementChild.innerText)
    elempot[i]=table[i].firstElementChild.innerText
  }
}
console.log(elempot)
window.localStorage.setItem("elempot",JSON.stringify(elempot))
