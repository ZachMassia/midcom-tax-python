class TaxEntry:
    max_label_len = 15

    def __init__(self, _id):
        self.id = _id
        self.tax_type = '$'
        self.tax_rate = '000000'
        self.tax_subtotal = 'N'
        self.label = 'NOT A VALID TX-'

    def get_rate(self):
        return self.tax_type + self.tax_rate + self.tax_subtotal


class Product:
    max_tax_count = 20

    def __init__(self, _id):
        self.id = _id
        self.taxes = ['00'] * Product.max_tax_count

    def get_tax_code(self):
        return ''.join(self.taxes)


class MIDCOM:
    tax_entry_count = 20
    product_count = 100

    def __init__(self):
        self.taxes = [TaxEntry(i) for i in range(MIDCOM.tax_entry_count)]
        self.products = [Product(i) for i in range(MIDCOM.product_count)]

        self.filename = ''

    def get_dat(self):
        rates = '\n'.join([tax.get_rate() for tax in self.taxes])
        labels = '\n'.join([tax.label for tax in self.taxes])
        products = '\n'.join([product.get_tax_code() for product in self.products])

        return '\n'.join([rates, labels, products])

    def get_str(self):
        # First character must be a 'T'
        output_str = 'TAX FILE FOR MIDCOM 8000. CREATED USING PYTHON APP BY ZACH MASSIA.'

        output_str += '+' * (510 - len(output_str))
        output_str += '\r\n'

        # Add the 20 tax rates, no separators or delimiters.
        output_str += ''.join([t.get_rate() for t in self.taxes])
        # Pad remaining 352 characters.
        output_str += '+' * 350
        output_str += '\r\n'

        # Add the 20 tax labels, no separators or delimiters.
        output_str += ''.join([t.label for t in self.taxes])
        # Pad remaining 212 chars.
        output_str += '+' * 210
        output_str += '\r\n'

        # Add the 100 tax combinations.
        # These must be entered in multiple blocks.
        #
        # 12 together, no separator, then a 32 character pad.
        # Repeat above sequence 8 times.
        #
        # Add final 4 sets with 352 character pad.
        # The final character must be '|'
        product_index = 0
        for _ in range(8):
            # Add the 12 combinations
            for _ in range(12):
                output_str += self.products[product_index].get_tax_code()
                product_index += 1
            # Add the 32 character pad.
            output_str += '+' * 30
            output_str += '\r\n'

        # The final 4 combinations.
        for _ in range(4):
            output_str += self.products[product_index].get_tax_code()
            product_index += 1
        output_str += '+' * 350
        output_str += '\r\n'

        output_str += '|'

        return output_str

    @staticmethod
    def write_file(filename, contents):
        with open(file=filename, mode='w', newline='') as file:
            file.write(contents)
