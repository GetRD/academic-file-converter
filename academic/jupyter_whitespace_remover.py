from nbconvert.preprocessors import Preprocessor


class JupyterWhitespaceRemover(Preprocessor):
    """
    Try to clean up a Jupyter notebook by:
     - removing blank code cells
     - removing unnecessary whitespace
    """

    def preprocess(self, nb, resources):
        """
        Remove blank `code` cells
        """
        for index, cell in enumerate(nb.cells):
            if cell.cell_type == "code" and not cell.source:
                nb.cells.pop(index)
            else:
                nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        return nb, resources

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Remove extraneous whitespace from code cells' source code
        """
        if cell.cell_type == "code":
            cell.source = cell.source.strip()

        return cell, resources
