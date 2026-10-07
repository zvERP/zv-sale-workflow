/** @odoo-module **/

import {
    prioritizeExactReferenceOptions,
} from "@sale_product_exact_reference_search/js/exact_reference_autocomplete";

QUnit.module("Sale product exact reference autocomplete", () => {
    QUnit.test("exact reference is placed before partial references", (assert) => {
        const options = [
            { value: 1, label: "[17857395] ESSENTIAL CAT MIXI 3KG" },
            { value: 2, label: "[10785] SUELO PLASTICO" },
            { value: 3, label: "[785] VITALAIT TOP 60" },
            { label: 'Create "785"' },
        ];

        const result = prioritizeExactReferenceOptions(options, "785");

        assert.deepEqual(
            result.map((option) => option.value || option.label),
            [3, 1, 2, 'Create "785"']
        );
    });

    QUnit.test("unmatched options keep their original order", (assert) => {
        const options = [
            { value: 1, label: "[17857395] ESSENTIAL CAT MIXI 3KG" },
            { value: 2, label: "[10785] SUELO PLASTICO" },
        ];

        assert.strictEqual(prioritizeExactReferenceOptions(options, "785"), options);
    });
});
