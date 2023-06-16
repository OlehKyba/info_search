from luqum.tree import AndOperation, Not, OrOperation, Word
from luqum.visitor import TreeTransformer


class OperationVisitor(TreeTransformer):
    def visit_and_operation(self, node: AndOperation, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].and_()

    def visit_or_operation(self, node: OrOperation, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].or_()

    def visit_not(self, node: Not, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].not_()

    def visit_word(self, node: Word, context: dict):
        yield from self.generic_visit(node, context)
        context["query_context"].term(node.value)
