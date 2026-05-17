import flet as ft
import flet.canvas as cv
import json

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.x = 0
        self.y = 0
        self.altura = 1

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        camino = []
        if self.raiz is None:
            self.raiz = Nodo(valor)
            camino.append(valor)
            return camino
        cola = [self.raiz]
        while cola:
            nodo = cola.pop(0)
            camino.append(nodo.valor)
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
                camino.append(valor)
                break
            else:
                cola.append(nodo.izquierdo)

            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
                camino.append(valor)
                break
            else:
                cola.append(nodo.derecho)
        return camino

    def eliminar(self, valor):
        if not self.raiz: return
        if self.raiz.valor == valor and not self.raiz.izquierdo and not self.raiz.derecho:
            self.raiz = None
            return
        nodo_a_eliminar = None
        temp = None
        cola = [self.raiz]
        while cola:
            temp = cola.pop(0)
            if temp.valor == valor: nodo_a_eliminar = temp
            if temp.izquierdo: cola.append(temp.izquierdo)
            if temp.derecho: cola.append(temp.derecho)
        if nodo_a_eliminar:
            ultimo_valor = temp.valor
            self._eliminar_ultimo(temp)
            nodo_a_eliminar.valor = ultimo_valor

    def _eliminar_ultimo(self, ultimo_nodo):
        cola = [self.raiz]
        while cola:
            nodo = cola.pop(0)
            if nodo is ultimo_nodo: return
            if nodo.derecho:
                if nodo.derecho is ultimo_nodo:
                    nodo.derecho = None
                    return
                cola.append(nodo.derecho)
            if nodo.izquierdo:
                if nodo.izquierdo is ultimo_nodo:
                    nodo.izquierdo = None
                    return
                cola.append(nodo.izquierdo)

    def buscar(self, valor):
        camino = []
        if not self.raiz: return camino, False
        cola = [self.raiz]
        while cola:
            nodo = cola.pop(0)
            camino.append(nodo.valor)
            if nodo.valor == valor: return camino, True
            if nodo.izquierdo: cola.append(nodo.izquierdo)
            if nodo.derecho: cola.append(nodo.derecho)
        return camino, False

    def calcular_posiciones(self, ancho_lienzo):
        if self.raiz is not None:
            self._calcular_coordenadas(self.raiz, 0, ancho_lienzo / 2, 50, ancho_lienzo / 4, 80)

    def _calcular_coordenadas(self, nodo, nivel, x, y, desplazamiento, espaciado_y):
        if nodo is not None:
            nodo.x = x
            nodo.y = y
            self._calcular_coordenadas(nodo.izquierdo, nivel + 1, x - desplazamiento, y + espaciado_y, desplazamiento / 2, espaciado_y)
            self._calcular_coordenadas(nodo.derecho, nivel + 1, x + desplazamiento, y + espaciado_y, desplazamiento / 2, espaciado_y)

    def serializar(self):
        def nodo_a_dict(nodo):
            if not nodo: return None
            return {"valor": nodo.valor, "izquierdo": nodo_a_dict(nodo.izquierdo), "derecho": nodo_a_dict(nodo.derecho)}
        return {"tipo": self.__class__.__name__, "raiz": nodo_a_dict(self.raiz)}

    def cargar_desde_dict(self, data):
        def dict_a_nodo(d):
            if not d: return None
            nodo = Nodo(d["valor"])
            nodo.izquierdo = dict_a_nodo(d.get("izquierdo"))
            nodo.derecho = dict_a_nodo(d.get("derecho"))
            return nodo
        self.raiz = dict_a_nodo(data.get("raiz"))

    def recorrido_preorder(self):
        resultado = []

        def _pre(nodo):
            if nodo:
                resultado.append(nodo.valor)
                _pre(nodo.izquierdo)
                _pre(nodo.derecho)
        _pre(self.raiz)
        return resultado

    def recorrido_inorder(self):
        resultado = []

        def _in(nodo):
            if nodo:
                _in(nodo.izquierdo)
                resultado.append(nodo.valor)
                _in(nodo.derecho)
        _in(self.raiz)
        return resultado

    def recorrido_postorder(self):
        resultado = []

        def _post(nodo):
            if nodo:
                _post(nodo.izquierdo)
                _post(nodo.derecho)
                resultado.append(nodo.valor)
        _post(self.raiz)
        return resultado

    def obtener_estadisticas(self):
        def contar_nodos(nodo):
            if not nodo: return 0
            return 1 + contar_nodos(nodo.izquierdo) + contar_nodos(nodo.derecho)

        def altura_arbol(nodo):
            if not nodo: return 0
            return 1 + max(altura_arbol(nodo.izquierdo), altura_arbol(nodo.derecho))
        nodos = contar_nodos(self.raiz)
        altura = altura_arbol(self.raiz)
        raiz_val = self.raiz.valor if self.raiz else "Ninguna"
        return nodos, altura, raiz_val

class ArbolBST(ArbolBinario):
    def insertar(self, valor):
        camino = []
        if self.raiz is None:
            self.raiz = Nodo(valor)
            camino.append(valor)
        else:
            self._insertar_recursivo(self.raiz, valor, camino)
        return camino

    def _insertar_recursivo(self, nodo, valor, camino):
        camino.append(nodo.valor)
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
                camino.append(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor, camino)
        elif valor > nodo.valor:
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
                camino.append(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor, camino)

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if not nodo: return nodo
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            if not nodo.izquierdo: return nodo.derecho
            if not nodo.derecho: return nodo.izquierdo
            temp = self._min_valor_nodo(nodo.derecho)
            nodo.valor = temp.valor
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, temp.valor)
        return nodo

    def _min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo: actual = actual.izquierdo
        return actual

    def buscar(self, valor):
        camino = []
        encontrado = self._buscar_recursivo(self.raiz, valor, camino)
        return camino, encontrado

    def _buscar_recursivo(self, nodo, valor, camino):
        if not nodo: return False
        camino.append(nodo.valor)
        if nodo.valor == valor: return True
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor, camino)
        else:
            return self._buscar_recursivo(nodo.derecho, valor, camino)

class ArbolAVL(ArbolBST):
    def _obtener_altura(self, nodo):
        if not nodo: return 0
        return nodo.altura

    def _obtener_balance(self, nodo):
        if not nodo: return 0
        return self._obtener_altura(nodo.izquierdo) - self._obtener_altura(nodo.derecho)

    def _rotacion_derecha(self, z):
        y = z.izquierdo
        T3 = y.derecho
        y.derecho = z
        z.izquierdo = T3
        z.altura = 1 + max(self._obtener_altura(z.izquierdo), self._obtener_altura(z.derecho))
        y.altura = 1 + max(self._obtener_altura(y.izquierdo), self._obtener_altura(y.derecho))
        return y

    def _rotacion_izquierda(self, z):
        y = z.derecho
        T2 = y.izquierdo
        y.izquierdo = z
        z.derecho = T2
        z.altura = 1 + max(self._obtener_altura(z.izquierdo), self._obtener_altura(z.derecho))
        y.altura = 1 + max(self._obtener_altura(y.izquierdo), self._obtener_altura(y.derecho))
        return y

    def insertar(self, valor):
        camino = []
        self.raiz = self._insertar_recursivo_avl(self.raiz, valor, camino)
        return camino

    def _insertar_recursivo_avl(self, nodo, valor, camino):
        if not nodo:
            camino.append(valor)
            return Nodo(valor)

        camino.append(nodo.valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo_avl(nodo.izquierdo, valor, camino)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo_avl(nodo.derecho, valor, camino)
        else:
            return nodo
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierdo), self._obtener_altura(nodo.derecho))
        balance = self._obtener_balance(nodo)
        if balance > 1 and valor < nodo.izquierdo.valor:
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor > nodo.derecho.valor:
            return self._rotacion_izquierda(nodo)
        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)
        return nodo

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo_avl(self.raiz, valor)

    def _eliminar_recursivo_avl(self, nodo, valor):
        if not nodo:
            return nodo
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo_avl(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo_avl(nodo.derecho, valor)
        else:
            if not nodo.izquierdo: return nodo.derecho
            if not nodo.derecho: return nodo.izquierdo
            temp = self._min_valor_nodo(nodo.derecho)
            nodo.valor = temp.valor
            nodo.derecho = self._eliminar_recursivo_avl(nodo.derecho, temp.valor)
        if not nodo: return nodo
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierdo), self._obtener_altura(nodo.derecho))
        balance = self._obtener_balance(nodo)
        if balance > 1 and self._obtener_balance(nodo.izquierdo) >= 0:
            return self._rotacion_derecha(nodo)
        if balance > 1 and self._obtener_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        if balance < -1 and self._obtener_balance(nodo.derecho) <= 0:
            return self._rotacion_izquierda(nodo)
        if balance < -1 and self._obtener_balance(nodo.derecho) > 0:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)
        return nodo

def main(page: ft.Page):
    page.title = "Visualizador de Árboles - Proyecto 2"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    mi_arbol = ArbolBST()
    lienzo = cv.Canvas(expand=True)
    estado_recorrido = {"secuencia": [], "paso_actual": -1, "activo": False}

    def mostrar_mensaje(mensaje):
        snack = ft.SnackBar(ft.Text(mensaje))
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def dibujar_arbol_en_lienzo(nodo):
        if nodo is not None:
            if nodo.izquierdo:
                lienzo.shapes.append(cv.Line(nodo.x, nodo.y, nodo.izquierdo.x, nodo.izquierdo.y, paint=ft.Paint(stroke_width=2, color=ft.Colors.WHITE54)))
                dibujar_arbol_en_lienzo(nodo.izquierdo)
            if nodo.derecho:
                lienzo.shapes.append(cv.Line(nodo.x, nodo.y, nodo.derecho.x, nodo.derecho.y, paint=ft.Paint(stroke_width=2, color=ft.Colors.WHITE54)))
                dibujar_arbol_en_lienzo(nodo.derecho)
            paso = estado_recorrido["paso_actual"]
            secuencia = estado_recorrido["secuencia"]
            es_actual = (estado_recorrido["activo"] and 0 <= paso < len(secuencia) and secuencia[paso] == nodo.valor)
            ya_visitado = (estado_recorrido["activo"] and 0 <= paso < len(secuencia) and nodo.valor in secuencia[:paso])
            if es_actual:
                lienzo.shapes.append(cv.Circle(nodo.x, nodo.y, 26, paint=ft.Paint(color=ft.Colors.WHITE_70)))
                lienzo.shapes.append(cv.Circle(nodo.x, nodo.y, 22, paint=ft.Paint(color=ft.Colors.GREEN_600)))
            elif ya_visitado:
                lienzo.shapes.append(cv.Circle(nodo.x, nodo.y, 20, paint=ft.Paint(color=ft.Colors.GREEN_900)))
            else:
                lienzo.shapes.append(cv.Circle(nodo.x, nodo.y, 20, paint=ft.Paint(color=ft.Colors.BLUE_700)))
            lienzo.shapes.append(cv.Text(nodo.x - 10, nodo.y - 10, str(nodo.valor), style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)))

    def actualizar_vista():
        lienzo.shapes.clear()
        if mi_arbol.raiz:
            ancho_disponible = page.width - 260 if page.width and page.width > 260 else 800
            mi_arbol.calcular_posiciones(ancho_disponible)
            dibujar_arbol_en_lienzo(mi_arbol.raiz)
        nodos, altura, raiz_val = mi_arbol.obtener_estadisticas()
        txt_stats.value = f"Nodos: {nodos} | Altura: {altura} | Raíz: {raiz_val}"
        _actualizar_panel_recorrido()
        page.update()

    def al_redimensionar(e):
        if mi_arbol.raiz:
            actualizar_vista()
    page.on_resize = al_redimensionar
    txt_stats = ft.Text("Nodos: 0 | Altura: 0 | Raíz: Ninguna", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.YELLOW_300)
    txt_recorrido_titulo = ft.Text("", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300)
    txt_recorrido_secuencia = ft.Text("", size=20, color=ft.Colors.WHITE70)
    txt_paso_actual = ft.Text("", size=20, color=ft.Colors.GREEN_400, weight=ft.FontWeight.BOLD)

    def _actualizar_panel_recorrido():
        if not estado_recorrido["activo"]:
            txt_recorrido_titulo.value = ""
            txt_recorrido_secuencia.value = ""
            txt_paso_actual.value = ""
            btn_siguiente.disabled = True
            btn_detener.disabled = True
        else:
            paso = estado_recorrido["paso_actual"]
            sec = estado_recorrido["secuencia"]
            total = len(sec)
            partes = []
            for i, v in enumerate(sec):
                if i < paso:
                    partes.append(f"[{v}]")
                elif i == paso:
                    partes.append(f" {v} ")
                else:
                    partes.append(str(v))
            txt_recorrido_secuencia.value = "  →  ".join(partes)
            if 0 <= paso < total:
                txt_paso_actual.value = f"Paso {paso + 1} / {total}  —  Nodo actual: {sec[paso]}"
            elif paso >= total:
                txt_paso_actual.value = f"Operación completada  ({total} nodos procesados)"
                txt_recorrido_secuencia.value = "  →  ".join(f"[{v}]" for v in sec)
            btn_siguiente.disabled = (paso >= total - 1)
            btn_detener.disabled = False

    def iniciar_animacion(titulo: str, secuencia: list):
        if not secuencia: return
        estado_recorrido["secuencia"] = secuencia
        estado_recorrido["paso_actual"] = 0
        estado_recorrido["activo"] = True
        txt_recorrido_titulo.value = titulo
        actualizar_vista()

    def btn_preorder_click(e):
        if mi_arbol.raiz is None: return mostrar_mensaje("Árbol vacío.")
        iniciar_animacion("Recorrido Pre-orden:", mi_arbol.recorrido_preorder())

    def btn_inorder_click(e):
        if mi_arbol.raiz is None: return mostrar_mensaje("Árbol vacío.")
        iniciar_animacion("Recorrido In-orden:", mi_arbol.recorrido_inorder())

    def btn_postorder_click(e):
        if mi_arbol.raiz is None: return mostrar_mensaje("Árbol vacío.")
        iniciar_animacion("Recorrido Post-orden:", mi_arbol.recorrido_postorder())

    def btn_siguiente_click(e):
        if not estado_recorrido["activo"]: return
        if estado_recorrido["paso_actual"] < len(estado_recorrido["secuencia"]) - 1:
            estado_recorrido["paso_actual"] += 1
        actualizar_vista()

    def btn_detener_click(e):
        estado_recorrido["activo"] = False
        estado_recorrido["secuencia"] = []
        estado_recorrido["paso_actual"] = -1
        actualizar_vista()

    def cambiar_tipo_arbol(e):
        nonlocal mi_arbol
        estado_recorrido["activo"] = False
        estado_recorrido["secuencia"] = []
        estado_recorrido["paso_actual"] = -1
        tipo = selector_arbol.value
        if tipo == "Binario":
            mi_arbol = ArbolBinario()
        elif tipo == "BST":
            mi_arbol = ArbolBST()
        elif tipo == "AVL":
            mi_arbol = ArbolAVL()
        actualizar_vista()

    async def btn_insertar_click(e):
        if not txt_valor.value: return
        try:
            valor = int(txt_valor.value)
            camino = mi_arbol.insertar(valor)
            txt_valor.value = ""
            iniciar_animacion("Ruta de Inserción:", camino)
        except ValueError:
            mostrar_mensaje("Por favor, ingresa un número válido.")

    async def btn_eliminar_click(e):
        if not txt_valor.value: return
        try:
            valor = int(txt_valor.value)
            mi_arbol.eliminar(valor)
            txt_valor.value = ""
            btn_detener_click(None)
        except ValueError:
            mostrar_mensaje("Por favor, ingresa un número válido.")

    async def btn_buscar_click(e):
        if not txt_valor.value: return
        try:
            valor = int(txt_valor.value)
            camino, encontrado = mi_arbol.buscar(valor)
            iniciar_animacion("Ruta de Búsqueda:", camino)
            if encontrado:
                mostrar_mensaje(f"Valor {valor} encontrado.")
            else:
                mostrar_mensaje(f"Valor {valor} no encontrado en el árbol.")
        except ValueError:
            mostrar_mensaje("Por favor, ingresa un número válido.")

    async def btn_guardar_click(e):
        if mi_arbol.raiz is None:
            return mostrar_mensaje("El árbol está vacío. Inserta nodos antes de guardar.")
        ruta = await ft.FilePicker().save_file(dialog_title="Guardar Árbol", file_name="mi_arbol.json", allowed_extensions=["json"])
        if ruta:
            if not ruta.endswith(".json"): ruta += ".json"
            with open(ruta, "w") as f:
                json.dump(mi_arbol.serializar(), f, indent=4)
            mostrar_mensaje("Árbol guardado exitosamente.")

    async def btn_cargar_click(e):
        nonlocal mi_arbol
        archivos = await ft.FilePicker().pick_files(dialog_title="Cargar Árbol", allowed_extensions=["json"])
        if archivos:
            with open(archivos[0].path, "r") as f:
                datos = json.load(f)
            tipo = datos.get("tipo", "ArbolBST")
            if tipo == "ArbolBinario":
                mi_arbol, selector_arbol.value = ArbolBinario(), "Binario"
            elif tipo == "ArbolBST":
                mi_arbol, selector_arbol.value = ArbolBST(), "BST"
            elif tipo == "ArbolAVL":
                mi_arbol, selector_arbol.value = ArbolAVL(), "AVL"
            mi_arbol.cargar_desde_dict(datos)
            selector_arbol.update()
            btn_detener_click(None)
            mostrar_mensaje("Árbol cargado exitosamente.")
    selector_arbol = ft.Dropdown(label="Tipo de Árbol", options=[ft.dropdown.Option("Binario"), ft.dropdown.Option("BST"), ft.dropdown.Option("AVL")], value="BST", width=180, on_select=cambiar_tipo_arbol)
    txt_valor = ft.TextField(label="Valor del Nodo", width=180)
    btn_insertar = ft.Button("Insertar", on_click=btn_insertar_click, width=180, icon=ft.Icons.ADD)
    btn_eliminar = ft.Button("Eliminar", on_click=btn_eliminar_click, width=180, icon=ft.Icons.DELETE)
    btn_buscar = ft.Button("Buscar", on_click=btn_buscar_click, width=180, icon=ft.Icons.SEARCH)
    btn_guardar = ft.Button("Guardar", on_click=btn_guardar_click, width=180, icon=ft.Icons.SAVE)
    btn_cargar = ft.Button("Cargar", on_click=btn_cargar_click, width=180, icon=ft.Icons.UPLOAD_FILE)
    btn_preorder = ft.Button("Pre-orden", on_click=btn_preorder_click, width=180)
    btn_inorder = ft.Button("In-orden", on_click=btn_inorder_click, width=180)
    btn_postorder = ft.Button("Post-orden", on_click=btn_postorder_click, width=180)
    btn_siguiente = ft.Button("Siguiente", on_click=btn_siguiente_click, width=180, disabled=True)
    btn_detener = ft.Button("Detener", on_click=btn_detener_click, width=180, disabled=True)
    panel_control = ft.Column([ft.Text("Controles", size=20, weight=ft.FontWeight.BOLD), selector_arbol, txt_valor, btn_insertar, btn_buscar, btn_eliminar, ft.Divider(), btn_guardar, btn_cargar, ft.Divider(), ft.Text("Recorridos", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_200), btn_preorder, btn_inorder, btn_postorder, ft.Divider(), btn_siguiente, btn_detener, ], width=200, scroll=ft.ScrollMode.AUTO)
    panel_recorrido = ft.Container(content=ft.Column([txt_stats, ft.Divider(height=2, color=ft.Colors.WHITE24), txt_recorrido_titulo, ft.Container(content=ft.Column([txt_recorrido_secuencia], scroll=ft.ScrollMode.ADAPTIVE), height=60), txt_paso_actual, ], spacing=4), bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE), border_radius=8, padding=10, margin=ft.Margin(left=0, top=8, right=0, bottom=0))
    page.add(ft.Row([panel_control, ft.Column([ft.Container(content=lienzo, bgcolor=ft.Colors.BLACK87, border_radius=10, expand=True, width=float("inf")), panel_recorrido, ], expand=True, spacing=10), ], expand=True))


ft.run(main)