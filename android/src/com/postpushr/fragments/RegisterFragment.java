package com.postpushr.fragments;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.postpushr.R;
import com.postpushr.Util;
import com.postpushr.fragments.SignInFragment.SignInListener;
import com.postpushr.model.Account;
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

		Button registerSubmitButton = (Button) view.findViewById(R.id.register_submit_button);
		registerSubmitButton.setOnClickListener(new RegisterSubmitListener());

		return view;
	}

	private class RegisterSubmitListener implements OnClickListener {
		@Override
		public void onClick(final View view) {
			// TODO Validate other info

			final String username = ((EditText) getView().findViewById(R.id.register_email_edittext)).getText().toString();
			final String password = ((EditText) getView().findViewById(R.id.register_password_edittext)).getText().toString();
			final String hashedSaltedPassword = Util.hashAndSaltPassword(password);
			final String name = ((EditText) getView().findViewById(R.id.register_name_edittext)).getText().toString();
			final String address = ((EditText) getView().findViewById(R.id.register_address_edittext)).getText().toString();

			String creditCardNumber = ((EditText) getView().findViewById(R.id.register_credit_card_number_edittext)).getText().toString();
			int creditCardExpirationMonth = Integer.parseInt(((EditText) getView().findViewById(
					R.id.register_credit_card_expiration_date_month_edittext)).getText().toString());
			int creditCardExpirationYear = Integer.parseInt(((EditText) getView().findViewById(
					R.id.register_credit_card_expiration_date_year_edittext)).getText().toString());
			String creditCardSecurityCode = ((EditText) getView().findViewById(R.id.register_credit_card_security_code_edittext)).getText()
					.toString();

			Card card = new Card(creditCardNumber, creditCardExpirationMonth, creditCardExpirationYear, creditCardSecurityCode);

			if (card.validateNumber() && card.validateCVC()) {

				Stripe stripe;
				try {
					stripe = new Stripe("pk_test_bRZoGvGajV5TeFq28CmFyxYa");
					stripe.createToken(card, new TokenCallback() {
						@Override
						public void onSuccess(Token token) {

							try {
								// TODO: validate the info with the server
								HttpClient httpclient = new DefaultHttpClient();
								HttpPost httppost = new HttpPost("http://postpushr.com/api/register");
								List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(5);
								nameValuePairs.add(new BasicNameValuePair("username", username));
								nameValuePairs.add(new BasicNameValuePair("password", password));
								nameValuePairs.add(new BasicNameValuePair("name", name));
								nameValuePairs.add(new BasicNameValuePair("address", address));
								nameValuePairs.add(new BasicNameValuePair("token", token.toString()));
								httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

								HttpResponse response = httpclient.execute(httppost);

								BufferedReader reader = new BufferedReader(new InputStreamReader(response.getEntity().getContent(), "UTF-8"));
								StringBuilder builder = new StringBuilder();
								for (String line = null; (line = reader.readLine()) != null;) {
									builder.append(line).append("\n");
								}
								JSONObject jsonObject = new JSONObject(builder.toString());

								if (jsonObject.get("status").equals("success")) {
									((SignInListener) getActivity()).moveToHomeFragment(new Account(username, hashedSaltedPassword, null));
								} else {
									Toast.makeText(getActivity(), "Registration failed. Check your info and try again.", Toast.LENGTH_LONG).show();
								}

							} catch (ClientProtocolException e) {
								// TODO Auto-generated catch block
							} catch (IOException e) {
								// TODO Auto-generated catch block
							} catch (JSONException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
						}

						@Override
						public void onError(Exception error) {
							// Show localized error message
							Toast.makeText(view.getContext(), error.getLocalizedMessage(), Toast.LENGTH_LONG).show();
						}
					});
				} catch (AuthenticationException e) {
					Toast.makeText(view.getContext(), "auth error", Toast.LENGTH_LONG).show();
				}

			} else {
				Toast.makeText(view.getContext(), "card didn't validate/check cvc", Toast.LENGTH_LONG).show();
			}
		}
	}

}