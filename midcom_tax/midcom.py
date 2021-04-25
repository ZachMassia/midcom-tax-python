class InvalidTaxFile(Exception):
    """Raised when there was an error parsing the user-loaded tax file."""


class TaxEntry:
    max_label_len = 15

    def __init__(self, _id):
        self.id = _id
        self.tax_type = '$'
        self.tax_rate = '000000'
        self.tax_subtotal = 'N'
        self.label = 'NOT A VALID TX-'

    def load_tax_tuple(self, tax):
        # Unpack tax tuple
        tax_type = tax[0]
        tax_rate = tax[1]
        tax_subtotal = tax[2]

        if tax_type is not None:
            if tax_type in ['$', '%']:
                self.tax_type = tax_type
            else:
                raise InvalidTaxFile(f'Invalid tax type: "{tax_type}"')

        if tax_rate is not None:
            if len(tax_rate) == 6:
                self.tax_rate = tax_rate
            else:
                raise InvalidTaxFile(f'Invalid tax rate: "{tax_rate}", length {len(tax_rate)} != 6.')

        if tax_subtotal is not None:
            if tax_subtotal in ['Y', 'N']:
                self.tax_subtotal = tax_subtotal
            else:
                raise InvalidTaxFile(f'Invalid subtotal modifier {tax_subtotal}, only "Y" or "N" valid.')

    def get_rate(self):
        return self.tax_type + self.tax_rate + self.tax_subtotal


class Product:
    max_tax_count = 20

    def __init__(self, _id):
        self.id = _id
        self.taxes = ['00'] * Product.max_tax_count

    def get_tax_code(self):
        return ''.join(self.taxes)

    def load_raw_str(self, raw_str):
        if len(raw_str) == Product.max_tax_count * 2:
            self.taxes = [raw_str[j:j+2] for j in range(0, Product.max_tax_count, 2)]
        else:
            raise InvalidTaxFile(
                f'Product tax combination improper length: {len(raw_str)}, should be {Product.max_tax_count*2}.'
            )


class MIDCOM:
    tax_entry_count = 20
    product_count = 100

    valid_dat_file_len = 4740
    valid_str_file_len = 6145

    def __init__(self):
        self.taxes = [TaxEntry(i) for i in range(MIDCOM.tax_entry_count)]
        self.products = [Product(i) for i in range(MIDCOM.product_count)]

        self.filename = ''

    def get_dat(self):
        rates = '\r\n'.join([tax.get_rate() for tax in self.taxes])
        labels = '\r\n'.join([tax.label for tax in self.taxes])
        products = '\r\n'.join([product.get_tax_code() for product in self.products])

        return '\r\n'.join([rates, labels, products, '\r\n'])

    def load_dat(self, contents):
        if len(contents) != MIDCOM.valid_dat_file_len:
            raise InvalidTaxFile(
                f'Could not load Cybercard tax file, length "{len(contents)} != {MIDCOM.valid_dat_file_len}"'
            )

        # Split file on newline.
        xs = contents.split('\r\n')

        # Get raw sections
        tax_strings = xs[0:MIDCOM.tax_entry_count]  # [0:20]
        label_strings = xs[MIDCOM.tax_entry_count:MIDCOM.tax_entry_count*2]  # [20:40]
        product_strings = xs[MIDCOM.tax_entry_count*2:]  # [40:EOF]

        # Split list of '$123456Y' into list of ('$', '123456', 'Y').
        taxes = [(t[0], t[1:7], t[7]) for t in tax_strings]

        # Setup tax objects.
        for i in range(MIDCOM.tax_entry_count):
            tax = self.taxes[i]
            tax.load_tax_tuple(taxes[i])
            tax.label = label_strings[i]

        # Setup product objects.
        for i in range(MIDCOM.product_count):
            prod = self.products[i]
            prod.load_raw_str(product_strings[i])

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

    def load_str(self, contents):
        raise InvalidTaxFile('Loading SD Card .str files not yet supported.')
