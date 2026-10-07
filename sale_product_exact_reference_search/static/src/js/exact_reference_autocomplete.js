/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";

export function prioritizeExactReferenceOptions(options, request) {
    const reference = request.trim();
    if (!reference) {
        return options;
    }

    const exactPrefix = `[${reference}]`;
    const isExactReference = (option) =>
        option.value &&
        (option.label === exactPrefix || option.label.startsWith(`${exactPrefix} `));
    const exactOptions = options.filter(isExactReference);
    if (!exactOptions.length) {
        return options;
    }
    return exactOptions.concat(options.filter((option) => !isExactReference(option)));
}

patch(
    Many2XAutocomplete.prototype,
    "sale_product_exact_reference_search.Many2XAutocomplete",
    {
        async loadOptionsSource(request) {
            const options = await this._super(...arguments);
            if (this.props.resModel !== "product.product") {
                return options;
            }
            return prioritizeExactReferenceOptions(options, request);
        },
    }
);
