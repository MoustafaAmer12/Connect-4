import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter
from PyQt5.QtCore import Qt


class TreeNode:
    """Represents a node in the tree."""
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []


class TreeGraphicsView(QGraphicsView):
    def __init__(self, root_node):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.draw_tree(root_node)

    def draw_tree(self, root_node):
        """Draws the tree starting from the root node using BFS for efficiency."""
        pen = QPen(Qt.black)
        pen.setWidth(2)
        node_radius = 25  # Radius of each node
        node_positions = {}  # Store calculated positions for nodes
        level_widths = {}  # Track the number of nodes at each level

        def calculate_positions():
            """Calculate positions for all nodes using BFS."""
            queue = [(root_node, 0, 0)]  # (node, level, index)
            max_level = 0

            while queue:
                node, level, index = queue.pop(0)
                max_level = max(max_level, level)

                # Track the number of nodes per level
                if level not in level_widths:
                    level_widths[level] = 0
                level_widths[level] += 1

                x_spacing = 100  # Horizontal spacing
                y_spacing = 100  # Vertical spacing
                total_width = level_widths[level] * x_spacing
                x_offset = 600 - total_width // 2  # Center nodes horizontally

                x = x_offset + index * x_spacing
                y = level * y_spacing
                node_positions[node] = (x, y)

                # Enqueue children with updated level and index
                for i, child in enumerate(node.children):
                    queue.append((child, level + 1, level_widths[level] - 1))

            return max_level

        def draw_node(node, x, y):
            """Draw a single node."""
            # Determine color based on node type
            if node.node_type == "MAX":
                color = QColor(220, 20, 60)  # Crimson
            elif node.node_type == "MIN":
                color = QColor(30, 144, 255)  # DodgerBlue
            elif node.node_type == "EXPECTATION":
                color = QColor(128, 128, 128)  # Gray
            else:
                color = QColor(240, 248, 255)  # AliceBlue

            brush = QBrush(color)
            ellipse = self.scene.addEllipse(
                x - node_radius,
                y - node_radius,
                2 * node_radius,
                2 * node_radius,
                pen,
                brush,
            )

            # Add a label with the node type and value
            label = f"{node.value}" if node.value is not None else node.node_type
            text = QGraphicsTextItem(label)
            text.setDefaultTextColor(Qt.black)
            text.setPos(x - 15, y - 15)
            self.scene.addItem(text)
            return ellipse

        def draw_edges():
            """Draw edges using stored positions."""
            for node, (x, y) in node_positions.items():
                for child in node.children:
                    if child in node_positions:
                        child_x, child_y = node_positions[child]
                        self.scene.addLine(x, y + node_radius, child_x, child_y - node_radius, pen)

        # Calculate positions and draw the tree
        max_level = calculate_positions()

        # Draw nodes
        for node, (x, y) in node_positions.items():
            draw_node(node, x, y)

        # Draw edges
        draw_edges()


def generate_tree(levels):
    """Generate a tree structure with exponential growth."""
    root = TreeNode(node_type="MAX", value=0)
    current_level = [root]

    for level in range(1, levels):
        next_level = []
        node_type = "MIN" if level % 2 == 0 else "MAX"
        for parent in current_level:
            for _ in range(7):  # Each node has 7 children
                child = TreeNode(node_type=node_type, value=level)
                parent.children.append(child)
                next_level.append(child)
        current_level = next_level

    return root


if __name__ == "__main__":
    # Generate tree with 6 levels
    root_node = generate_tree(levels=7)

    app = QApplication(sys.argv)
    view = TreeGraphicsView(root_node)
    view.setWindowTitle("Dynamic Tree Drawer")
    view.resize(1200, 800)
    view.show()
    sys.exit(app.exec_())
