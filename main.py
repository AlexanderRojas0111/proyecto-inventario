import tkinter as tk
from tkinter import ttk, messagebox
from app.inventory import update_inventory
from app.sales import register_sale, add_sale_detail
from app.purchases import register_purchase, add_purchase_detail
from app.reports import generate_sales_report
from app.user_management import authenticate_user

class GestionInventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("800x600")

        self.user = authenticate_user("admin@example.com", "password")
        if not self.user:
            messagebox.showerror("Error", "Autenticación fallida.")
            root.destroy()
            return

        self.create_menu()
        self.create_content_frame()

    def create_menu(self):
        frame_menu = ttk.Frame(self.root, padding=10)
        frame_menu.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(frame_menu, text="Actualizar Inventario", command=self.show_update_inventory).pack(side=tk.LEFT)
        ttk.Button(frame_menu, text="Registrar Venta", command=self.show_register_sale).pack(side=tk.LEFT)
        ttk.Button(frame_menu, text="Registrar Compra", command=self.show_register_purchase).pack(side=tk.LEFT)
        ttk.Button(frame_menu, text="Generar Reporte", command=self.show_generate_report).pack(side=tk.LEFT)

    def create_content_frame(self):
        self.content_frame = ttk.Frame(self.root, padding=10)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_update_inventory(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Actualizar Inventario", font=("Arial", 16)).pack()

        ttk.Label(self.content_frame, text="ID del producto:").pack()
        product_id_entry = ttk.Entry(self.content_frame)
        product_id_entry.pack()

        ttk.Label(self.content_frame, text="Cantidad:").pack()
        quantity_entry = ttk.Entry(self.content_frame)
        quantity_entry.pack()

        ttk.Label(self.content_frame, text="Tipo de movimiento (Entrada/Salida):").pack()
        movement_type_entry = ttk.Entry(self.content_frame)
        movement_type_entry.pack()

        ttk.Label(self.content_frame, text="Descripción del movimiento:").pack()
        description_entry = ttk.Entry(self.content_frame)
        description_entry.pack()

        ttk.Label(self.content_frame, text="Documento de referencia:").pack()
        reference_document_entry = ttk.Entry(self.content_frame)
        reference_document_entry.pack()

        def update():
            try:
                product_id = product_id_entry.get()
                quantity = quantity_entry.get()
                movement_type = movement_type_entry.get()
                description = description_entry.get()
                reference_document = reference_document_entry.get()

                if not product_id or not quantity or not movement_type or not description or not reference_document:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return

                update_inventory(product_id, int(quantity), movement_type, self.user["name"], description, reference_document)
                messagebox.showinfo("Info", "Inventario actualizado.")
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser un número entero.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar el inventario: {e}")

        ttk.Button(self.content_frame, text="Actualizar", command=update).pack()

    def show_register_sale(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Registrar Venta", font=("Arial", 16)).pack()

        ttk.Label(self.content_frame, text="Nombre del cliente:").pack()
        client_entry = ttk.Entry(self.content_frame)
        client_entry.pack()

        ttk.Label(self.content_frame, text="Método de pago:").pack()
        payment_method_entry = ttk.Entry(self.content_frame)
        payment_method_entry.pack()

        sale_details_frame = ttk.Frame(self.content_frame)
        sale_details_frame.pack()

        sale_details = []

        def add_detail():
            try:
                product_id = product_id_entry.get()
                quantity = int(quantity_entry.get())
                price_unit = float(price_unit_entry.get())
                discount = float(discount_entry.get())
                subtotal = quantity * price_unit - discount
                sale_details.append((product_id, quantity, price_unit, subtotal, discount))
                messagebox.showinfo("Info", "Detalle añadido.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores válidos para cantidad, precio unitario y descuento.")

        ttk.Label(sale_details_frame, text="ID del producto:").grid(row=0, column=0)
        product_id_entry = ttk.Entry(sale_details_frame)
        product_id_entry.grid(row=0, column=1)

        ttk.Label(sale_details_frame, text="Cantidad:").grid(row=1, column=0)
        quantity_entry = ttk.Entry(sale_details_frame)
        quantity_entry.grid(row=1, column=1)

        ttk.Label(sale_details_frame, text="Precio unitario:").grid(row=2, column=0)
        price_unit_entry = ttk.Entry(sale_details_frame)
        price_unit_entry.grid(row=2, column=1)

        ttk.Label(sale_details_frame, text="Descuento:").grid(row=3, column=0)
        discount_entry = ttk.Entry(sale_details_frame)
        discount_entry.grid(row=3, column=1)

        ttk.Button(sale_details_frame, text="Añadir detalle", command=add_detail).grid(row=4, columnspan=2)

        def register():
            try:
                sale_id = register_sale(client_entry.get(), payment_method_entry.get(), self.user["name"])
                for detail in sale_details:
                    add_sale_detail(sale_id, *detail)
                messagebox.showinfo("Info", "Venta registrada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")

        ttk.Button(self.content_frame, text="Registrar", command=register).pack()

    def show_register_purchase(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Registrar Compra", font=("Arial", 16)).pack()

        ttk.Label(self.content_frame, text="Nombre del proveedor:").pack()
        supplier_entry = ttk.Entry(self.content_frame)
        supplier_entry.pack()

        purchase_details_frame = ttk.Frame(self.content_frame)
        purchase_details_frame.pack()

        purchase_details = []

        def add_detail():
            try:
                product_id = product_id_entry.get()
                quantity = int(quantity_entry.get())
                price_unit = float(price_unit_entry.get())
                subtotal = quantity * price_unit
                purchase_details.append((product_id, quantity, price_unit, subtotal))
                messagebox.showinfo("Info", "Detalle añadido.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores válidos para cantidad y precio unitario.")

        ttk.Label(purchase_details_frame, text="ID del producto:").grid(row=0, column=0)
        product_id_entry = ttk.Entry(purchase_details_frame)
        product_id_entry.grid(row=0, column=1)

        ttk.Label(purchase_details_frame, text="Cantidad:").grid(row=1, column=0)
        quantity_entry = ttk.Entry(purchase_details_frame)
        quantity_entry.grid(row=1, column=1)

        ttk.Label(purchase_details_frame, text="Precio unitario:").grid(row=2, column=0)
        price_unit_entry = ttk.Entry(purchase_details_frame)
        price_unit_entry.grid(row=2, column=1)

        ttk.Button(purchase_details_frame, text="Añadir detalle", command=add_detail).grid(row=3, columnspan=2)

        def register():
            try:
                product_id = product_id_entry.get()
                quantity = int(quantity_entry.get())
                price_unit = float(price_unit_entry.get())
                cost = quantity * price_unit  # Calcular el costo
                purchase_id = register_purchase(product_id, quantity, supplier_entry.get(), cost)  # Llamar con los parámetros correctos

                for detail in purchase_details:
                    add_purchase_detail(purchase_id, *detail)
                messagebox.showinfo("Info", "Compra registrada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la compra: {e}")

        ttk.Button(self.content_frame, text="Registrar", command=register).pack()

    def show_generate_report(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Generar Reporte", font=("Arial", 16)).pack()

        ttk.Label(self.content_frame, text="Fecha de inicio (YYYY-MM-DD):").pack()
        start_date_entry = ttk.Entry(self.content_frame)
        start_date_entry.pack()

        ttk.Label(self.content_frame, text="Fecha de fin (YYYY-MM-DD):").pack()
        end_date_entry = ttk.Entry(self.content_frame)
        end_date_entry.pack()

        def generate():
            report = generate_sales_report(start_date_entry.get(), end_date_entry.get())
            messagebox.showinfo("Reporte Generado", report)

        ttk.Button(self.content_frame, text="Generar", command=generate).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionInventarioApp(root)
    root.mainloop()
