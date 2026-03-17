import csv
import ezdxf
import os

class LayerExporter:
    def __init__(self, drawing_path):
        self.drawing_path = drawing_path
        self.layers = []

    def load_layers(self):
        """Load layers from the provided AutoCAD drawing."""
        try:
            doc = ezdxf.readfile(self.drawing_path)
            self.layers = list(doc.layers)
        except IOError:
            print(f"Error: File {self.drawing_path} not found.")
            return False
        except ezdxf.DXFError:
            print(f"Error: The file {self.drawing_path} is not a valid DXF file.")
            return False
        return True

    def export_to_csv(self, output_path):
        """Export the loaded layers to a CSV file."""
        if not self.layers:
            print("No layers to export. Please load layers first.")
            return

        try:
            with open(output_path, mode='w', newline='') as csvfile:
                fieldnames = ['Layer Name', 'Color', 'Linetype', 'Visible']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for layer in self.layers:
                    writer.writerow({
                        'Layer Name': layer.dxf.name,
                        'Color': layer.dxf.color,
                        'Linetype': layer.dxf.linetype,
                        'Visible': not layer.is_off(),
                    })
            print(f"Layers exported successfully to {output_path}.")
        except Exception as e:
            print(f"Error writing to CSV: {e}")

def main():
    drawing_path = input("Enter the path to the AutoCAD drawing (DXF file): ")
    output_path = input("Enter the output CSV file path: ")

    exporter = LayerExporter(drawing_path)
    
    if exporter.load_layers():
        exporter.export_to_csv(output_path)

if __name__ == "__main__":
    main()

# TODO: 
# - Add support for different DXF versions
# - Implement command-line arguments for better usability
# - Add unit tests for the LayerExporter class
# - Improve error handling with more specific exceptions
# - Consider adding more layer properties to export
