list = document.querySelectorAll('.TableGrid tr')
output = ""
list.forEach(item=>{
    data=[
        item.querySelector('td:nth-of-type(2)').innerText,
        item.querySelector('td:nth-of-type(4)').innerText, // size
        item.querySelector('td:nth-of-type(5)').innerText, // chromosome in database
        item.querySelector('td:nth-of-type(8)').innerText // assemblies
    ]
    if(parseInt(data[3]) >= 1)
        output+= (data.join("\t").replaceAll(" ", ""))+"\n"
})
output

