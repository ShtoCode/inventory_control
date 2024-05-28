
const radioButtons = document.querySelectorAll('input[name="filter-radio"]')
radioButtons.forEach((radioButton) => {
  radioButton.addEventListener('click', async () => {
    history.pushState({}, document.title, window.location.pathname)
    const selectedFilter = radioButton.value
    const currentUrl = new URL(window.location.href)
    currentUrl.searchParams.set('filter', selectedFilter)
    window.location.href = currentUrl.toString()
  })
})

const search = document.getElementById("table-search-products")
search.addEventListener('keypress', () => {
  if (event.key == 'Enter') {
    history.pushState({}, document.title, window.location.pathname)
    const valueSearch = search.value
    const currentUrl = new URL(window.location.href)
    currentUrl.searchParams.set('search', valueSearch)
    window.location.href = currentUrl.toString()
  }
})

const form = document.getElementById("add-product");
const addProduct = async (e) => {
  try {
    e.preventDefault();
    const formData = new FormData(form);
    const response = await fetch("/admin/add-product", {
      method: "POST",
      body: formData
    })
    const result = await response.json()
    if (response.status == 200) {
      Swal.fire({
        title: "¡Producto agregado!",
        icon: "success",
        position: "center",
        showConfirmButton: false,
        timer: 1000
      })
        .then(
          setTimeout(() => {
            location.reload()
          }, 1000)
        )
    } else {
      Swal.fire({
        title: "¡Error al registrar el producto!",
        text: result.message,
        icon: "error",
        position: "center",
        showConfirmButton: true,
        confirmButtonColor: "#6afe3b"
      })
    }

  }
  catch (err) {
    console.error(err);
  }
}

const editProduct = async (e) => {
  try {
    e.preventDefault();

    const editForm = e.target
    const formData = new FormData(editForm);
    const idProducto = formData.get('id-product')
    const response = await fetch("/admin/edit-product/" + idProducto, {
      method: "POST",
      body: formData
    })
    const result = await response.json()
    if (response.status == 200) {
      Swal.fire({
        title: "¡Producto modificado!",
        icon: "success",
        position: "center",
        showConfirmButton: false,
        timer: 1000,
        confirmButtonColor: "#4b7579"
      })
        .then(
          setTimeout(() => {
            location.reload()
          }, 1000)
        )

    } else {
      Swal.fire({
        title: "¡Error al modificar el producto!",
        text: result.message,
        icon: "error",
        position: "center",
        showConfirmButton: true,
        confirmButtonColor: "#4b7579"
      })
    }

  }
  catch (err) {
    console.error(err);
  }
}


const setNoDisponible = async (e) => {
  e.preventDefault()
  const button = e.target
  const idProducto = button.getAttribute('data-producto-id');
  console.log(idProducto)
  Swal.fire({
    title: "¿Quieres desactivar este producto?",
    showCancelButton: true,
    icon: "question",
    confirmButtonText: "Sí",
    confirmButtonColor: "#4b7579",
    cancelButtonText: "No",
    cancelButtonColor: "#ff333f"
  }).then(async (result) => {
    if (result.isConfirmed) {
      const response = await fetch(`/admin/disable/${idProducto}`, {
        method: 'POST'
      });

      if (response.status == 200) {
        Swal.fire({
          title: "¡Producto desactivado!",
          showConfirmButton: false,
          icon: "success",
          timer: 1500
        })
          .then(
            setTimeout(() => {
              location.reload()
            }, 1000)
          )
      } else {
        console.error('Error al desactivar el producto: ', response.statusText)
      }
    }
  })
}

const setDisponible = async (e) => {
  e.preventDefault()
  const button = e.target
  const idProducto = button.getAttribute('data-producto-id');
  console.log(idProducto)
  Swal.fire({
    title: "¿Quieres activar este producto?",
    text: "Asegurate de que el producto tenga stock disponible.",
    showCancelButton: true,
    icon: "question",
    confirmButtonText: "Sí",
    confirmButtonColor: "#4b7579",
    cancelButtonText: "No",
    cancelButtonColor: "#ff333f"
  }).then(async (result) => {
    if (result.isConfirmed) {
      const response = await fetch(`/admin/enable/${idProducto}`, {
        method: 'POST'
      });

      if (response.status == 200) {
        Swal.fire({
          title: "¡Producto activado!",
          showConfirmButton: false,
          icon: "success",
          timer: 1500
        })
          .then(
            setTimeout(() => {
              location.reload()
            }, 1000)
          )
      } else {
        Swal.fire({
          title: "¡Error al activar el producto!",
          icon: "error",
          position: "center",
          showConfirmButton: true,
          confirmButtonColor: "#4b7579"
        })
      }
    }
  })
}

