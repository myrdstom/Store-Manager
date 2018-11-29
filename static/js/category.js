document.getElementById('getText').addEventListener('click', getCategories);
document.getElementById('deleteSingleText').addEventListener('click', deleteSingleCategory);
function getCategories(){
    fetch('http://127.0.0.1:5000/api/v1/categories',{
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
                data.forEach(function (category) {
                    output += `
                <table>
                <tbody>
                <tr >
                <td>${category.category_id}</td>
                <td class = "category-list-group-item">${category.category_name}</td>

                </tr>
                </tbody>
                </table>
                `;
                });


                document.getElementById('output').innerHTML = output;
            }

        })

    }
function deleteSingleCategory(e){
    e.preventDefault();
    let categoryid = document.getElementById('myInput').value;
    let category_id = parseInt(categoryid);
    if (isNaN(category_id)){
        alert("Please insert an ID")
    }

    fetch('http://127.0.0.1:5000/api/v1/categories/' + category_id,{
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
