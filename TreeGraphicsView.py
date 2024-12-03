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
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.scale_factor = 1.1

        self.setStyleSheet("""
            border: 2px solid #333;
            background-color: #c3c3c3;
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
        """)
        self.setMinimumHeight(400)
        self.setMaximumHeight(600)

        self.draw_tree(root_node)


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


    def draw_tree(self, root_node):
        """Draws the tree starting from the root node using BFS for efficiency."""
        if not root_node:
            return
        pen = QPen(QColor("black"))
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

            offset_x = start_x
            if node.children:
                for child in node.children:
                    child_width = calculate_subtree_width(child)
                    calculate_positions(child, offset_x + (child_width * horizontal_spacing) // 2, y + vertical_spacing, total_width)
                    offset_x += child_width * horizontal_spacing

        def draw_node(node, x, y):
            """Draw a single node."""
            # Determine color based on node type
            color = {
                "MAX": QColor(220, 20, 60),  # Crimson
                "MIN": QColor(30, 144, 255),  # DodgerBlue
                "EXPECTATION": QColor(128, 128, 128),  # Gray
            }.get(node.type, QColor(240, 248, 255))  # Default AliceBlue

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


        calculate_positions(root_node, 600, 50, 1200)
        for node, (x, y) in node_positions.items():
            draw_node(node, x, y)
        draw_edges()