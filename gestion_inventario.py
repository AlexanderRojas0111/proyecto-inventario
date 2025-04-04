import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class InventoryMediator(ABC):
    """Interfaz para el mediador del sistema de inventario"""
    @abstractmethod
    def update_inventory(self, product_id: str, quantity: int, movement_type: str, 
                        user: str, description: str, reference_document: str) -> bool:
        pass
    
    @abstractmethod
    def register_sale(self, client: str, payment_method: str, 
                     details: List[Dict[str, Any]]) -> bool:
        pass
    
    @abstractmethod
    def register_purchase(self, supplier: str, 
                         details: List[Dict[str, Any]]) -> bool:
        pass
    
    @abstractmethod
    def generate_report(self, start_date: str, end_date: str, 
                       report_type: str = "PDF") -> Any:
        pass

class InventoryMediatorImpl(InventoryMediator):
    """Implementación concreta del mediador de inventario"""
    def __init__(self):
        from inventory import update_inventory, adjust_inventory
        from sales import register_sale, add_sale_detail
        from purchases import register_purchase, add_purchase_detail
        from reports import ReportGenerator, PDFReportStrategy
        
        self.update_inventory_fn = update_inventory
        self.adjust_inventory_fn = adjust_inventory
        self.register_sale_fn = register_sale
        self.add_sale_detail_fn = add_sale_detail
        self.register_purchase_fn = register_purchase
        self.add_purchase_detail_fn = add_purchase_detail
        self.report_generator = ReportGenerator(PDFReportStrategy())
    
    def update_inventory(self, product_id: str, quantity: int, movement_type: str, 
                        user: str, description: str, reference_document: str) -> bool:
        try:
            self.update_inventory_fn(
                product_id, quantity, movement_type, 
                user, description, reference_document
            )
            return True
        except Exception as e:
            print(f"Error en mediador al actualizar inventario: {e}")
            return False
    
    def register_sale(self, client: str, payment_method: str, 
                     details: List[Dict[str, Any]]) -> bool:
        try:
            sale_id = self.register_sale_fn(client, payment_method, "Sistema")
            for detail in details:
                self.add_sale_detail_fn(
                    sale_id, 
                    detail["product_id"],
                    detail["quantity"],
                    detail["price_unit"],
                    detail["discount"]
                )
                # Actualizar inventario (salida)
                self.update_inventory(
                    detail["product_id"],
                    detail["quantity"],
                    "Salida",
                    "Sistema",
                    f"Venta #{sale_id}",
                    f"Venta-{sale_id}"
                )
            return True
        except Exception as e:
            print(f"Error en mediador al registrar venta: {e}")
            return False
    
    def register_purchase(self, supplier: str, 
                         details: List[Dict[str, Any]]) -> bool:
        try:
            purchase_id = self.register_purchase_fn(supplier, "Sistema")
            for detail in details:
                self.add_purchase_detail_fn(
                    purchase_id,
                    detail["product_id"],
                    detail["quantity"],
                    detail["price_unit"]
                )
                # Actualizar inventario (entrada)
                self.update_inventory(
                    detail["product_id"],
                    detail["quantity"],
                    "Entrada",
                    "Sistema",
                    f"Compra #{purchase_id}",
                    f"Compra-{purchase_id}"
                )
            return True
        except Exception as e:
            print(f"Error en mediador al registrar compra: {e}")
            return False
    
    def generate_report(self, start_date: str, end_date: str, 
                       report_type: str = "PDF") -> Any:
        try:
            return self.report_generator.generate_report(start_date, end_date)
        except Exception as e:
            print(f"Error en mediador al generar reporte: {e}")
            return None

class GestionInventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.root.geometry("800x600")
        
        # Crear instancia del mediador
        self.mediator = InventoryMediatorImpl()
        
        self.create_menu()
        self.create_content_frame()

    def create_menu(self):
        frame_menu = ttk.Frame(self.root, padding=10)
        frame_menu.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(frame_menu, text="Actualizar Inventario", 
                  command=self.show_update_inventory).pack(side=tk.LEFT)
        ttk.Button(frame_menu, text="Registrar Venta", 
                  command=self.show_register_sale).pack(side=tk.LEFT)
        ttk.Button(frame_menu, text="Registrar Compra", 
                  command=self.show_register_purchase).pack(side=tk.LEFT)
        ttk.Button(frame_menu, text="Generar Reporte", 
                  command=self.show_generate_report).pack(side=tk.LEFT)

    def create_content_frame(self):
        self.content_frame = ttk.Frame(self.root, padding=10)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_update_inventory(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Actualizar Inventario", 
                 font=("Arial", 16)).pack()

        # Campos del formulario (igual que antes)
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

        def update_inventory_handler():
            try:
                product_id = product_id_entry.get()
                quantity = quantity_entry.get()
                movement_type = movement_type_entry.get()
                description = description_entry.get()
                reference_document = reference_document_entry.get()

                if not product_id or not quantity or not movement_type or not description or not reference_document:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.")
                    return

                success = self.mediator.update_inventory(
                    product_id, int(quantity), movement_type, 
                    "Sistema", description, reference_document
                )
                
                if success:
                    messagebox.showinfo("Info", "Inventario actualizado.")
                else:
                    messagebox.showerror("Error", "Error al actualizar inventario.")
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser un número entero.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar el inventario: {e}")

        ttk.Button(self.content_frame, text="Actualizar", 
                  command=update_inventory_handler).pack()

    def show_register_sale(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Registrar Venta", 
                 font=("Arial", 16)).pack()

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
                
                sale_details.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "price_unit": price_unit,
                    "discount": discount
                })
                messagebox.showinfo("Info", "Detalle añadido.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores válidos para cantidad, precio unitario y descuento.")

        # Campos para detalles de venta (igual que antes)
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

        ttk.Button(sale_details_frame, text="Añadir detalle", 
                  command=add_detail).grid(row=4, columnspan=2)

        def register_sale_handler():
            try:
                if not sale_details:
                    messagebox.showerror("Error", "Debe añadir al menos un detalle de venta.")
                    return
                
                success = self.mediator.register_sale(
                    client_entry.get(),
                    payment_method_entry.get(),
                    sale_details
                )
                
                if success:
                    messagebox.showinfo("Info", "Venta registrada.")
                else:
                    messagebox.showerror("Error", "Error al registrar la venta.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")

        ttk.Button(self.content_frame, text="Registrar", 
                  command=register_sale_handler).pack()

    def show_register_purchase(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Registrar Compra", 
                 font=("Arial", 16)).pack()

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
                
                purchase_details.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "price_unit": price_unit
                })
                messagebox.showinfo("Info", "Detalle añadido.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores válidos para cantidad y precio unitario.")

        # Campos para detalles de compra (igual que antes)
        ttk.Label(purchase_details_frame, text="ID del producto:").grid(row=0, column=0)
        product_id_entry = ttk.Entry(purchase_details_frame)
        product_id_entry.grid(row=0, column=1)

        ttk.Label(purchase_details_frame, text="Cantidad:").grid(row=1, column=0)
        quantity_entry = ttk.Entry(purchase_details_frame)
        quantity_entry.grid(row=1, column=1)

        ttk.Label(purchase_details_frame, text="Precio unitario:").grid(row=2, column=0)
        price_unit_entry = ttk.Entry(purchase_details_frame)
        price_unit_entry.grid(row=2, column=1)

        ttk.Button(purchase_details_frame, text="Añadir detalle", 
                  command=add_detail).grid(row=3, columnspan=2)

        def register_purchase_handler():
            try:
                if not purchase_details:
                    messagebox.showerror("Error", "Debe añadir al menos un detalle de compra.")
                    return
                
                success = self.mediator.register_purchase(
                    supplier_entry.get(),
                    purchase_details
                )
                
                if success:
                    messagebox.showinfo("Info", "Compra registrada.")
                else:
                    messagebox.showerror("Error", "Error al registrar la compra.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la compra: {e}")

        ttk.Button(self.content_frame, text="Registrar", 
                  command=register_purchase_handler).pack()

    def show_generate_report(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Generar Reporte", 
                 font=("Arial", 16)).pack()

        ttk.Label(self.content_frame, text="Fecha de inicio (YYYY-MM-DD):").pack()
        start_date_entry = ttk.Entry(self.content_frame)
        start_date_entry.pack()

        ttk.Label(self.content_frame, text="Fecha de fin (YYYY-MM-DD):").pack()
        end_date_entry = ttk.Entry(self.content_frame)
        end_date_entry.pack()

        def generate_report_handler():
            try:
                report = self.mediator.generate_report(
                    start_date_entry.get(),
                    end_date_entry.get()
                )
                messagebox.showinfo("Reporte Generado", report)
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar el reporte: {e}")

        ttk.Button(self.content_frame, text="Generar", 
                  command=generate_report_handler).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionInventarioApp(root)
    root.mainloop()
