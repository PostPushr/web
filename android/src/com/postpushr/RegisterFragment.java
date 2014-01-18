package com.postpushr;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.stripe.android.Stripe;
import com.stripe.android.TokenCallback;
import com.stripe.android.model.Card;
import com.stripe.android.model.Token;
import com.stripe.exception.AuthenticationException;

public class RegisterFragment extends Fragment {

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		getActivity().setTitle("Register");
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup parent, Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.fragment_register, parent, false);

		Button submitButton = (Button) view.findViewById(R.id.register_submit_button);
		submitButton.setOnClickListener(new RegisterSubmitListener()); 

		return view;
	}

	private class RegisterSubmitListener implements OnClickListener {
		@Override
		public void onClick(final View view) {
			// TODO Validation

			String creditCardNumber = ((EditText) getView().findViewById(R.id.register_credit_card_number_edittext)).getText().toString();
			int creditCardExpirationMonth = Integer.parseInt(((EditText) getView().findViewById(R.id.register_credit_card_expiration_date_month_edittext)).getText().toString());
			int creditCardExpirationYear = Integer.parseInt(((EditText) getView().findViewById(R.id.register_credit_card_expiration_date_year_edittext)).getText().toString());
			String creditCardSecurityCode = ((EditText) getView().findViewById(R.id.register_credit_card_security_code_edittext)).getText().toString();

			Card card = new Card(creditCardNumber, creditCardExpirationMonth, creditCardExpirationYear, creditCardSecurityCode);

			if (card.validateNumber() && card.validateCVC()) {

				Stripe stripe;
				try {
					stripe = new Stripe(Util.getStripeKey());
					stripe.createToken(
							card,
							new TokenCallback() {
								public void onSuccess(Token token) {
									// Send token to your server
									Toast.makeText(view.getContext(),
											"Made it werk. Now make it twerk",
											Toast.LENGTH_LONG
											).show();
								}
								public void onError(Exception error) {
									// Show localized error message
									Toast.makeText(view.getContext(),
											error.getLocalizedMessage(),
											Toast.LENGTH_LONG
											).show();
								}
							}
							);
				} catch (AuthenticationException e) {
					Toast.makeText(view.getContext(),
							"auth error",
							Toast.LENGTH_LONG
							).show();
				}

			} else {
				Toast.makeText(view.getContext(),
						"card didn't validate/check cvc",
						Toast.LENGTH_LONG
						).show();
			}
		}
	}

}