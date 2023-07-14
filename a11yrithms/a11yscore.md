---
layout: page
---

# A11yScore

The A11yScore is a sophisticated tool that evaluates the accessibility of a set of URLs under a specific domain. By considering various severity levels of both violations and passes, the algorithm offers a composite score that reflects the accessibility status of the analyzed URLs. While excelling in identifying and weighting accessibility issues based on their severity and frequency, the score's accuracy and utility may depend on the quality and characteristics of the input data. It's important to note that this score may not entirely capture the user experience of individuals with disabilities.

## Variables

These are options which are used to select which URLs are used to generate the results.

| Variable       | Description                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| domain         | The domain within which the URLs are located.                                                              |
| axe tag        | Specific axe-core rule tags (e.g., wcag2a, wcag2aa) to filter the rules applied.                           |
| transformation | The type of transformation to apply to the data. Options include "logarithmic", "exponential", and "none". |

## Severity Levels

These static weights are applied to each of the severity levels. By assigning weights to different violation or pass types, the algorithm recognizes that not all accessibility issues impact users equally.

| Severity Level | Description                            |
| -------------- | -------------------------------------- |
| Sc             | severity of critical violations/passes |
| Ss             | severity of serious violations/passes  |
| Sm             | severity of moderate violations/passes |
| Smn            | severity of minor violations/passes    |

## Input Values

These are generated from the list of urls.

### Violations

| Variable | Description                  |
| -------- | ---------------------------- |
| Cv       | count of critical violations |
| Sv       | count of serious violations  |
| Mv       | count of moderate violations |
| mnv      | count of minor violations    |

### Passes

| Variable | Description              |
| -------- | ------------------------ |
| Cp       | count of critical passes |
| Sp       | count of serious passes  |
| Mp       | count of moderate passes |
| mnp      | count of minor passes    |

### Meta

| Variable | Description            |
| -------- | ---------------------- |
| U        | count of URLs analyzed |

### Resolved Values

| Variable | Description               |
| -------- | ------------------------- |
| Vt       | count of total violations |
| Pt       | count of total passes     |

## Normalization

Normalization is used to adjust the counts of violations and passes, making them comparable across different scales. This step is crucial as it ensures that large counts of violations or passes don't disproportionately influence the final score.

## Transformation

### Logarithmic Transformation

In the event of a "logarithmic" transformation selection, a logarithmic transformation is applied to the counts of violations and passes. By doing so, the algorithm compresses the scale of these values, reducing the effect of very large counts. This transformation is particularly useful when dealing with skewed data, as it can help reveal patterns that would otherwise be obscured.

### Exponential Transformation

In the event of an "exponential" transformation selection, an exponential transformation is applied to the weights derived from each violation or pass. This transformation amplifies differences, placing greater emphasis on high-frequency violations or passes. It serves to enhance the visibility of frequent accessibility issues.

## Weighting

Weighting is a critical step that balances the frequency of violations and passes against their severity. This prevents the score from being overly influenced by either high-frequency, low-severity issues or low-frequency, high-severity issues.

### Violations

| Variable | Description                |
| -------- | -------------------------- |
| Wc       | critical violations weight |
| Ws       | serious violations weight  |
| Wm       | moderate violations weight |
| Wmn      | minor violations weight    |

### Passes

| Variable | Description            |
| -------- | ---------------------- |
| Wcp      | critical passes weight |
| Wsp      | serious passes weight  |
| Wmp      | moderate passes weight |
| Wmnp     | minor passes weight    |

## Weight Calculation Formulae

The calculation of weights depends on the selected transformation. If "logarithmic" transformation is selected, the counts are transformed before being used in weight calculation. If "exponential" transformation is selected, the resulting weights are transformed.

### Transformation | None

```python
Wc = Sc * (1 / (Cv / Vt))
Ws = Ss * (1 / (Sv / Vt))
Wm = Sm * (1 / (Mv / Vt))
Wmn = Smn * (1 / (mnv / Vt))
Wcp = Sc * (1 / (Cp / Pt))
Wsp = Ss * (1 / (Sp / Pt))
Wmp = Sm * (1 / (Mp / Pt))
Wmnp = Smn * (1 / (mnp / Pt))
```

### Transformation | Logarithmic

```python
Wc = Sc * (1 / np.exp(np.log(Cv + 1) / Vt))
Ws = Ss * (1 / np.exp(np.log(Sv + 1) / Vt))
Wm = Sm * (1 / np.exp(np.log(Mv + 1) / Vt))
Wmn = Smn * (1 / np.exp(np.log(mnv + 1) / Vt))
Wcp = Sc * (1 / np.exp(np.log(Cp + 1) / Pt))
Wsp = Ss * (1 / np.exp(np.log(Sp + 1) / Pt))
Wmp = Sm * (1 / np.exp(np.log(Mp + 1) / Pt))
Wmnp = Smn * (1 / np.exp(np.log(mnp + 1) / Pt))
```

### Transformation | Exponential

```python
Wc = Sc * np.exp((1 / (Cv + 1) / Vt))
Ws = Ss * np.exp((1 / (Sv + 1) / Vt))
Wm = Sm * np.exp((1 / (Mv + 1) / Vt))
Wmn = Smn * np.exp((1 / (mnv + 1) / Vt))
Wcp = Sc * np.exp((1 / (Cp + 1) / Pt))
Wsp = Ss * np.exp((1 / (Sp + 1) / Pt))
Wmp = Sm * np.exp((1 / (Mp + 1) / Pt))
Wmnp = Smn * np.exp((1 / (mnp + 1) / Pt))
```

## Final Algorithm

The final score is computed using the weights derived from violations and passes. This score reflects the weighted difference between the violations and passes, normalized by the total number of URLs analyzed.

```python
Score = [(CvWc + SvWs + MvWm + mnvWmn) - (CpWcp + SpWsp + MpWmp + mnpWmnp)] / U
```
