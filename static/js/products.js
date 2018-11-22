document.getElementById('getText').addEventListener('click', getProducts);
       document.getElementById('getSingleText').addEventListener('click', getSingleProducts);
       document.getElementById('deleteSingleText').addEventListener('click', deleteSingleProducts);
        //document.getElementById('filterItem').addEventListener('submit', getSingleProduct);


        function deleteSingleProducts(e){
            e.preventDefault();
            let productid = document.getElementById('myInput').value;
            let product_id = parseInt(productid);
            console.log(product_id);
            if (isNaN(product_id)){
                alert("Please insert an ID")
            }

            fetch('http://127.0.0.1:5000/api/v1/products/' + product_id,{
                method: 'DELETE',
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
                    }

                })

        }



        function getSingleProducts(e){
            e.preventDefault();
            let productid = document.getElementById('myInput').value;
            let product_id = parseInt(productid);
            console.log(product_id);
            if (isNaN(product_id)){
                alert("Please insert an ID")
            }

            fetch('http://127.0.0.1:5000/api/v1/products/' + product_id,{
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
                        result.forEach(function (product) {
                            output += `
                        <table>
                        <tbody>
                        <tr >
                        <td class = "prod-list-group-item-5">${product.product_id}</td>
                        <td class = "prod-list-group-item-1">${product.product_name}</td>
                        <td class = "prod-list-group-item-2">${product.unit_price}</td>
                        <td class = "prod-list-group-item-3">${product.stock}</td>
                        <td class = "prod-list-group-item-4">${product.category_name}</td>
                        </tr>
                        </tbody>
                        </table>
                        `;
                        });


                        document.getElementById('output').innerHTML = output;

                    }

                })

        }

        function getProducts(){
            fetch('http://127.0.0.1:5000/api/v1/products',{
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
                        data.forEach(function (product) {
                            output += `
                        <table>
                        <tbody>
                        <tr >
                        <td class = "prod-list-group-item-5">${product.product_id}</td>
                        <td class = "prod-list-group-item-1">${product.product_name}</td>
                        <td class = "prod-list-group-item-2">${product.unit_price}</td>
                        <td class = "prod-list-group-item-3">${product.stock}</td>
                        <td class = "prod-list-group-item-4">${product.category_name}</td>
                        </tr>
                        </tbody>
                        </table>
                        `;
                        });


                        document.getElementById('output').innerHTML = output;
                    }

                })

        }