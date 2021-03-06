from textwrap import wrap

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

    def load_user_input_str(self, user_str: str):
        str_len = len(user_str)

        # Full length, split and use as is.
        if str_len > Product.max_tax_count * 2:
            raise InvalidTaxFile(f'User entry error. Product combination code too long: {str_len}')
        elif str_len == Product.max_tax_count * 2:
            self.taxes = [user_str[j:j+2] for j in range(0, Product.max_tax_count, 2)]
        else:
            # Make sure even number of digits
            if len(user_str) % 2 != 0:
                raise InvalidTaxFile(f'User entry error. Products must be in sets of 2 digits.')

            # Clear out previous list of tax codes
            self.taxes = ['00'] * Product.max_tax_count

            xs = [user_str[j:j+2] for j in range(0, str_len, 2)]
            for i in range(len(xs)):
                tax = xs[i]

                # Make sure numeric only.
                try:
                    int(tax)
                except ValueError as e:
                    raise InvalidTaxFile(f'User entry error. Not a number: {tax}') from e

                self.taxes[i] = tax

    def load_raw_str(self, raw_str: str):
        if len(raw_str) == Product.max_tax_count * 2:
            self.taxes = [raw_str[j:j+2] for j in range(0, Product.max_tax_count * 2, 2)]
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

        return '\r\n'.join([rates, labels, products, ''])

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
        if len(contents) != MIDCOM.valid_str_file_len:
            raise InvalidTaxFile(
                f'Could not load SD tax file, length "{len(contents)} != {MIDCOM.valid_str_file_len}"'
            )
        
        # Grab the 20 tax rates.
        i = 512
        rate_len = 8
        tax_rate_str = contents[i:i+(MIDCOM.tax_entry_count*rate_len)]

        # Split into array of tax rates.
        tax_strings = [tax_rate_str[i:i+rate_len] for i in range(0, len(tax_rate_str), rate_len)]

        # Split list of '$123456Y' into list of ('$', '123456', 'Y').
        taxes = [(t[0], t[1:7], t[7]) for t in tax_strings]

        # Grab the 100 product combinations.
        i = 1536
        comb_len = 40
        products = []

        for _ in range(0, 8):
            products.extend(wrap(
                contents[i:i+(12*comb_len)],
                comb_len
            ))
            i += 512

        # Grab remaining 4 entries not included in above loop.
        products.extend(wrap(
            contents[i:i+(4*comb_len)],
            comb_len
        ))

        # Grab the 20 labels.
        i = 1024
        label_len = 15
        label_str = contents[i:i+(MIDCOM.tax_entry_count*label_len)]

        # Split into array of labels.
        label_strings = [label_str[i:i+label_len] for i in range(0, len(label_str), label_len)]

        # Setup tax objects.
        for i in range(MIDCOM.tax_entry_count):
            tax = self.taxes[i]
            tax.load_tax_tuple(taxes[i])
            tax.label = label_strings[i]

        # Setup product objects.
        for i in range(MIDCOM.product_count):
            prod = self.products[i]
            prod.load_raw_str(products[i])