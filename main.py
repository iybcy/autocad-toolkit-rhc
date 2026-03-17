import sys
import os
import ezdxf

def export_layers_to_csv(drawing_file, output_file):
    """Export layers from DXF file to CSV"""
    try:
        doc = ezdxf.readfile(drawing_file)
        layers = doc.layers
        
        with open(output_file, 'w', newline='') as csvfile:
            csvfile.write('Layer Name,Color,Linetype,Lineweight,Plot\n')
            for layer in layers:
                csvfile.write(f'{layer.dxf.name},{layer.dxf.color},{layer.dxf.linetype},{layer.dxf.lineweight},{layer.dxf.plot}\n')
    except Exception as e:
        raise Exception(f'Error processing drawing file: {str(e)}')

def main():
    # Check if the user provided the necessary arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <drawing_file.dxf> <output_file.csv>")
        print("Note: This tool supports DXF files only. Convert DWG to DXF first.")
        sys.exit(1)

    drawing_file = sys.argv[1]
    output_file = sys.argv[2]

    # Validate the input drawing file
    if not os.path.isfile(drawing_file):
        print(f"Error: The file {drawing_file} does not exist.")
        sys.exit(1)
    
    # Check file extension
    if not drawing_file.lower().endswith('.dxf'):
        print("Error: Only DXF files are supported. Please convert DWG to DXF first.")
        sys.exit(1)

    # Attempt to export layers to CSV
    try:
        export_layers_to_csv(drawing_file, output_file)
        print(f"Successfully exported layers to {output_file}")
    except Exception as e:
        print(f"Failed to export layers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
