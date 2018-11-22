document.getElementById('getText').addEventListener('click', getSales);
document.getElementById('getSingleText').addEventListener('click', getSingleSales);
document.getElementById("addItem").addEventListener("submit", addProduct);

function getSingleSales(e){
    e.preventDefault();
    let saleid = document.getElementById('myInput').value;
    let sale_id = parseInt(saleid);
    console.log(sale_id);
    if (isNaN(sale_id)){
        alert("Please insert an ID")
    }
    fetch('http://127.0.0.1:5000/api/v1/sales/' + sale_id,{
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json'
        }
    })

        .then((res) => res.json())
            //console.log(res.json());
        .then((data) => {
            console.log(data);
            let result = [];
            result.push(data);
            console.log(result);



            if("msg" in data){
                alert(data.msg)
            }
            if ("message" in data){
                alert(data.message)
            } else {
                let output = '<h2> </h2>';
                result.forEach(function (sale) {
                    output += `
                    <table>
                    <tbody>
                    <tr >
                    <td class = "sale-list-group-item-5">${sale.sale_id}</td>
                    <td class = "sale-list-group-item-1">${sale.username}</td>
                    <td class = "sale-list-group-item-2">${sale.product_name}</td>
                    <td class = "sale-list-group-item-3">${sale.quantity}</td>
                    <td class = "sale-list-group-item-4">${sale.total}</td>
                    </tr>
                    </tbody>
                    </table>
                    `;
                });


                document.getElementById('output').innerHTML = output;
            }

        })
        .catch((err) => console.log(err))

}
function getSales(){
    fetch('http://127.0.0.1:5000/api/v1/sales',{
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json'
        }
    })

        .then((res) => res.json())
            //console.log(res.json());
        .then((data) => {
            console.log(data);

            if("msg" in data){
                alert(data.msg)
            }
            if ("message" in data){
                alert(data.message)
            } else {
                let output = '<h2> </h2>';
                data.forEach(function (sale) {
                    output += `
                <table>
                <tbody>
                <tr >
                <td class = "sale-list-group-item-5">${sale.sale_id}</td>
                <td class = "sale-list-group-item-1">${sale.username}</td>
                <td class = "sale-list-group-item-2">${sale.product_name}</td>
                <td class = "sale-list-group-item-3">${sale.quantity}</td>
                <td class = "sale-list-group-item-4">${sale.total}</td>
                </tr>
                </tbody>
                </table>
                `;
                });


                document.getElementById('output').innerHTML = output;
            }

        })

        }

function addProduct(e) {
 e.preventDefault();
let product_name = document.getElementById('pname').value;
let quantity_name = document.getElementById('qname').value;
let quantity = parseInt(quantity_name);


fetch('http://127.0.0.1:5000/api/v1/sales', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json'
        },
        body: JSON.stringify({
            product_name: product_name,
            quantity: quantity
        })
    })
 .then((res) => res.json())
 .then((data) => {
      console.log(data);
      if ("message" in data){
          alert(data.message)
      }

 });


}