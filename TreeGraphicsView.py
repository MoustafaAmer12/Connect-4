import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

from Agents.Node import Node

class TreeGraphicsView(QGraphicsView):
    def __init__(self, root_node):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.draw_tree(root_node)
        self.scale_factor = 1.1


    def wheelEvent(self, event):
        """Handle zoom in and zoom out using the mouse wheel."""
        if event.angleDelta().y() > 0:
            self.scale(self.scale_factor, self.scale_factor)  # Zoom in
        else:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)  # Zoom out


    def update_tree(self, new_root_node):
        self.root_node = new_root_node
        self.scene.clear()
        self.draw_tree(new_root_node)

    def wheelEvent(self, event):
        """Handle zoom in and zoom out using the mouse wheel."""
        if event.angleDelta().y() > 0:
            self.scale(self.scale_factor, self.scale_factor)  # Zoom in
        else:
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)  # Zoom out

    def draw_tree(self, root_node):
        """Draws the tree starting from the root node using BFS for efficiency."""
        pen = QPen(Qt.black)
        pen.setWidth(2)
        node_radius = 25  # Radius of each node
        node_positions = {}  # Store calculated positions for nodes

        horizontal_spacing = 80  # Horizontal spacing between nodes
        vertical_spacing = 120  # Vertical spacing between levels

        def calculate_subtree_width(node):
            """Recursively calculate the width of the subtree rooted at this node."""
            if not node.children:
                return 1
            return sum(calculate_subtree_width(child) for child in node.children)

        def calculate_positions(node, x, y, total_width):
            """Calculate positions for all nodes using DFS."""
            subtree_width = calculate_subtree_width(node)
            start_x = x - (subtree_width * horizontal_spacing) // 2  # Center subtree horizontally
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
            self.scene.addEllipse(
                x - node_radius,
                y - node_radius,
                2 * node_radius,
                2 * node_radius,
                pen,
                brush,
            )

            # Add a label with the node type and value
            label = f"{node.value}" if node.value is not None else node.type
            text = QGraphicsTextItem(label)
            text.setDefaultTextColor(QColor("black"))
            text.setPos(x - 15, y - 15)
            self.scene.addItem(text)

        def draw_edges():
            """Draw edges using stored positions."""
            for node, (x, y) in node_positions.items():
                if node.children:
                    for child in node.children:
                        if child in node_positions:
                            child_x, child_y = node_positions[child]
                            self.scene.addLine(x, y + node_radius, child_x, child_y - node_radius, pen)

        # Calculate positions and draw the tree
        max_level = calculate_positions()

        # Draw nodes
        for node, (x, y) in node_positions.items():
            draw_node(node, x, y)
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
